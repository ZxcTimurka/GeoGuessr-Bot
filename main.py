import asyncio
import os
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from check_coords import check
from config import TOKEN
from db import search_by_coords, search_by_id
from get_distance import getDistance
from get_image import getImages, getImage
from online_db import (add_player, print_curr_img, update_curr_img, update_time_bool, print_time_bool,
                       print_ready, update_search, update_pair, update_score, print_rating, update_suggest_stage,
                       print_suggest_stage)
from suggested_db import add_suggested_score, add_photo_name, print_id

token = TOKEN
bot = AsyncTeleBot(token)

if __name__ == '__main__':
    @bot.message_handler(commands=['start'])
    async def start_message(message):
        name = message.from_user.first_name

        add_player(message.chat.id, name)
        text = f'Привет, {name}!'
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton('Играть', callback_data='play'),
                   InlineKeyboardButton('Рейтинг', callback_data='rate'))
        markup.row(InlineKeyboardButton('Добавить локацию', callback_data='add'))
        await bot.send_message(message.chat.id, text, reply_markup=markup)


    @bot.callback_query_handler(func=lambda call: True)
    async def callback_query(call):
        if call.data == "back":
            await game_mods(call.message)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == 'play':
            await game_mods(call.message)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == 'classic_mode':
            await classic_mode(call.message)
            if call.message.content_type != 'photo':
                await bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == 'time_mode':
            text = ('У тебя будет *одна* минута на отгадывание как можно большего числа картинок. Нажми *продолжить* '
                    'чтобы начать игру!')
            markup = InlineKeyboardMarkup()
            markup.row(InlineKeyboardButton('Продолжить', callback_data='start_time_mod'))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode="Markdown")
        elif call.data == 'start_time_mod':
            update_time_bool(call.message.chat.id, 1)
            await timer(call.message)
            if call.message.content_type != 'photo':
                await bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == 'online_mode':
            text = '*Поиск соперников...*'
            update_search(call.message.chat.id, 1)
            await bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            search = asyncio.create_task(online_search(call.message))
            await asyncio.gather(search)
        elif call.data == 'rate':
            players = print_rating()
            players = sorted(players, key=lambda x: x, reverse=True)
            text = '\n'.join(sorted([f'{i + 1}. {j[0]} баллов - {j[1]}' for i, j in enumerate(players)]))
            await bot.send_message(call.message.chat.id, text)
        elif call.data == 'add':
            update_suggest_stage(call.message.chat.id, 1)
            await bot.send_message(call.message.chat.id, 'Отлично, теперь отправь мне фотографию локации,'
                                                         ' которую ты хочешь предложить!😀😀😀')


    @bot.message_handler(content_types=['location'])
    async def fgh_message(message):
        if not print_curr_img(message.chat.id)[0]:
            await bot.send_message(message.chat.id, 'Cначала нажми кнопку /start и выбери режим')
            return
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Назад', callback_data='play'),
                   InlineKeyboardButton('Продолжить', callback_data='classic_mode'))
        msg = tuple([message.location.latitude, message.location.longitude])
        name = [i for i in
                ''.join(print_curr_img(message.chat.id)).replace('images/', '').replace('.jpeg', '').split(', ')]
        name = search_by_id(name[0])
        answer = list(getDistance(*name, *msg))
        if print_time_bool(message.chat.id):
            if answer[0] == 0:
                answer[0] = -5
            answer[0] *= 2
        await bot.send_photo(message.chat.id, check(name, msg),
                             caption=f'Ты получил баллов: {answer[0]}. \n{answer[1]} - {search_by_coords(*name)[0]}',
                             reply_markup=markup)
        update_score(message.chat.id, answer[0])
        update_curr_img(message.chat.id, None)


    @bot.message_handler(content_types=['photo'])
    async def ask_text(message):
        if print_suggest_stage(message.chat.id) == 1:
            await bot.send_message(message.chat.id,
                                   'Замечательно😁! Теперь отправь мне координаты данного места вида: широта, долгота')
            with open(f'suggested_locations/{message.chat.id}.jpeg', 'wb') as photo:
                file_info = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
                downloaded_file = await bot.download_file(file_info.file_path)
                photo.write(downloaded_file)
            update_suggest_stage(message.chat.id, 2)


    @bot.message_handler(content_types=['text'])
    async def asd_message(message):
        if print_suggest_stage(message.chat.id) == 2:
            add_suggested_score(message.chat.id, *message.text.split(', '))
            await bot.send_message(message.chat.id,
                                   'Самое сложное позади, теперь просто напиши название этого места😎')
            update_suggest_stage(message.chat.id, 3)
        elif print_suggest_stage(message.chat.id) == 3:
            print(message.text, message.chat.id)
            print(print_id(message.chat.id, message.text))
            os.rename(f'suggested_locations/{message.chat.id}.jpeg',
                      f'suggested_locations/{print_id(message.chat.id, message.text)}.jpeg')
            add_photo_name(message.text, message.chat.id)
            await bot.send_message(message.chat.id, '😘')


    async def game_mods(message):
        text = 'Отлично! Выбери режим игры😉'
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton('Обычный', callback_data='classic_mode'),
                   InlineKeyboardButton('На время', callback_data='time_mode'),
                   InlineKeyboardButton('Онлайн', callback_data='online_mode'))
        markup.row(InlineKeyboardButton('Описание режимов', callback_data='des_game_mode'))
        await bot.send_message(message.chat.id, text, reply_markup=markup)


    async def classic_mode(message):
        photo = open(getImage(), 'rb')
        update_curr_img(message.chat.id, photo.name)
        print(print_curr_img(message.chat.id))
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Вернуться назад', callback_data='play'))
        await bot.send_photo(message.chat.id, photo, caption='Отправь мне координаты этого места', reply_markup=markup)


    async def time_mod(message):
        photo = open(getImage(), 'rb')
        update_curr_img(message.chat.id, photo.name)
        markup = InlineKeyboardMarkup()
        markup_lose = InlineKeyboardMarkup()
        markup_lose.add(InlineKeyboardButton('Начать заново', callback_data='time_mode'),
                        InlineKeyboardButton('Выбрать режим', callback_data='play'))
        await bot.send_photo(message.chat.id, photo, caption='Отправь мне координаты этого места!!!',
                             reply_markup=markup)


    async def timer(message):
        await time_mod(message)
        await asyncio.sleep(20)
        update_curr_img(message.chat.id, None)
        update_time_bool(message.chat.id, 0)
        await bot.send_message(message.chat.id, f'*Время вышло!*\nОтгаданных картинок: {0}', parse_mode="Markdown")


    async def online_search(message):
        await asyncio.sleep(5 + len(print_ready() * 2))
        if message.chat.id in print_ready():
            for i in print_ready():
                if i != message.chat.id:
                    print(message.chat.id, print_ready(), i)
                    update_pair(message.chat.id, i)
                    update_search(print_ready()[0], 0)
                    update_search(message.chat.id, 0)
                    await bot.send_message(message.chat.id, f'Я нашел игрока! {i}')
                    await bot.send_message(i, f'Я нашел игрока!{message.chat.id}')
                    await online_mode(message, i)
        if message.chat.id in print_ready():
            await bot.send_message(message.chat.id, 'Я никого не нашел😭😭😭')
            update_search(message.chat.id, 0)


    async def online_mode(message, id_enemy):
        photo = getImage()
        update_curr_img(message.chat.id, photo.replace('.jpeg', '').replace('images/', ''))
        update_curr_img(id_enemy, photo.replace('.jpeg', '').replace('images/', ''))
        print(print_curr_img(message.chat.id))
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Вернуться назад', callback_data='play'))
        await bot.send_photo(id_enemy, open(photo, 'rb'), caption='Отправь мне координаты этого места',
                             reply_markup=markup)
        await bot.send_photo(message.chat.id, open(photo, 'rb'), caption='Отправь мне координаты этого места',
                             reply_markup=markup)

asyncio.run(bot.polling())
