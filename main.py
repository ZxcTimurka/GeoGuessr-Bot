import time

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.async_telebot import AsyncTeleBot
import asyncio
import aioschedule as schedule
from check_coords import check
from config import TOKEN
from get_distance import getDistance
from get_image import getImages, getImage
from online_db import add_player, print_curr_img, update_curr_img, update_time_bool, print_time_bool, print_ready, update_search, update_pair, print_pair
from db import search_by_coords
import threading

token = TOKEN
bot = AsyncTeleBot(token)
time_dict = {}

if __name__ == '__main__':
    @bot.message_handler(commands=['start'])
    async def start_message(message):
        name = message.from_user.first_name
        add_player(message.chat.id, name, 0, 0, 0)
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
        if call.data == 'classic_mode':
            await classic_mode(call.message)
            if call.message.content_type != 'photo':
                await bot.delete_message(call.message.chat.id, call.message.message_id)
        if call.data == 'time_mode':
            text = 'У тебя будет *одна* минута на отгадывание как можно большего числа картинок. Нажми *продолжить* чтобы начать игру!'
            markup = InlineKeyboardMarkup()
            markup.row(InlineKeyboardButton('Продолжить', callback_data='start_time_mod'))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode="Markdown")
        if call.data == 'start_time_mod':
            update_time_bool(call.message.chat.id, 1)
            await timer(call.message)
            if call.message.content_type != 'photo':
                await bot.delete_message(call.message.chat.id, call.message.message_id)
        if call.data == 'online_mode':
            text = '*Поиск соперников...*'
            update_search(call.message.chat.id, 1)
            await bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            search = asyncio.create_task(online_search(call.message))
            await asyncio.gather(search)


    @bot.message_handler(content_types=['location'])
    async def fgh_message(message):
        print(print_curr_img(message.chat.id)[0])
        print('ok')

        if not print_curr_img(message.chat.id)[0]:
            await bot.send_message(message.chat.id, 'Cначала нажми кнопку /start')
            return
        # print(print_time_bool(message.chat.id))
        # if print_time_bool(message.chat.id):
        #     update_time_bool(message.chat.id, False)
        #     await bot.send_message(message.chat.id, 'Время вышло')
        #     await game_mods()
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Назад', callback_data='play'),
                   InlineKeyboardButton('Продолжить', callback_data='classic_mode'))
        msg = tuple([message.location.latitude, message.location.longitude])
        name = tuple([float(i) for i in
                      ''.join(print_curr_img(message.chat.id)).replace('images/', '').replace('.jpeg', '').split(
                          ', ')])
        await bot.send_photo(message.chat.id, check(name, msg),
                             caption=f'{getDistance(*name, *msg)} - {search_by_coords(*name)[0]}', reply_markup=markup)
        update_curr_img(message.chat.id, None)


    @bot.message_handler(content_types=['text'])
    async def asd_message(message):
        if message.text.isdigit():
            try:
                imgs = getImages(int(message.text))
                await bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(i) for i in imgs])
            except ValueError:
                await bot.send_message(message.chat.id, 'Неверный ввод')


    async def game_mods(message):
        text = 'Отлично! Выбери режим игры😉'
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton('Обычный', callback_data='classic_mode'),
                   InlineKeyboardButton('На время', callback_data='time_mode'),
                   InlineKeyboardButton('Онлайн', callback_data='online_mode'))
        markup.row(InlineKeyboardButton('Описание режимов', callback_data='des_game_mode'))
        await bot.send_message(message.chat.id, text, reply_markup=markup)


    async def classic_mode(message):
        photo = getImage()
        update_curr_img(message.chat.id, photo.name)
        print(print_curr_img(message.chat.id))
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Вернуться назад', callback_data='play'))
        await bot.send_photo(message.chat.id, photo, caption='Отправь мне координаты этого места', reply_markup=markup)


    # здесь не работает
    async def time_mod(message):
        photo = getImage()
        update_curr_img(message.chat.id, photo.name)
        markup = InlineKeyboardMarkup()
        markup_lose = InlineKeyboardMarkup()
        markup_lose.add(InlineKeyboardButton('Начать заново', callback_data='time_mode'),
                        InlineKeyboardButton('Выбрать режим', callback_data='play'))
        await bot.send_photo(message.chat.id, photo, caption='Отправь мне координаты этого места!!!', reply_markup=markup)


    async def timer(message):
        await time_mod(message)
        await asyncio.sleep(20)
        update_curr_img(message.chat.id, None)
        update_time_bool(message.chat.id, 0)
        await bot.send_message(message.chat.id, f'*Время вышло!*\nОтгаданных картинок: {0}', parse_mode="Markdown")


    async def online_search(message):
        for i in range(60):
            await asyncio.sleep(1)
            if print_ready() and print_ready()[0] != message.chat.id:
                await bot.send_message(message.chat.id, 'Я нашел игрока!')
                await bot.send_message(print_ready()[0], 'Я нашел игрока!')
                await update_pair(message.chat.id, print_ready()[0])
                return print_ready()[0]


asyncio.run(bot.polling())
