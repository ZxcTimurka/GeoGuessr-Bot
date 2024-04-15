import asyncio
import os

from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from check_coords import check
from config import TOKEN
from db import search_by_coords, search_by_id, next_id, add_location
from get_distance import getDistance
from get_image import getImage, getImages
from online_db import (add_player, print_curr_img, update_curr_img, update_time_bool, print_time_bool,
                       print_ready, update_search, update_pair, print_pair, update_score, print_rating,
                       update_suggest_stage,
                       print_suggest_stage, print_name, update_online_imgs, print_online_imgs, clear_pair)
from suggested_db import add_suggested_score, add_photo_name, print_id, get_all, delete_img

token = TOKEN
bot = AsyncTeleBot(token)
admins_id = [919813235, 1040654665, 1081575937]

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
        if message.chat.id in admins_id:
            markup.row(InlineKeyboardButton('Админ панель', callback_data='admin_panel'))
        await bot.send_message(message.chat.id, text, reply_markup=markup)


    @bot.callback_query_handler(func=lambda call: True)
    async def callback_query(call):
        global data, suggest
        if call.data == "back":
            await game_mods(call.message)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == 'back1':
            await start_message(call.message)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            update_suggest_stage(call.message.chat.id, 0)
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
            event = asyncio.Event()
            timer_task = asyncio.create_task(online_timer(call.message.chat.id))  # Запускаем таймер на 10 секунд
            loop_task = asyncio.create_task(online_search(event, call.message))  # Запускаем бесконечный цикл
            if await timer_task:
                event.set()
            await loop_task
        elif call.data == 'rate':
            players = print_rating()
            players = sorted(players, key=lambda x: x, reverse=True)
            text = '\n'.join(sorted([f'{i + 1}. {j[0]} баллов - {j[1]}' for i, j in enumerate(players)]))
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('Назад', callback_data='back1'))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == 'add':
            update_suggest_stage(call.message.chat.id, 1)
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('Назад', callback_data='back1'))
            await bot.send_message(call.message.chat.id, 'Отлично, теперь отправь мне фотографию локации,'
                                                         ' которую ты хочешь предложить!😀😀😀', reply_markup=markup)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == 'confirm':
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            os.replace(f'suggested_locations/{suggest[0]}.jpeg', f'images/{next_id()}.jpeg')
            add_location(suggest[2], suggest[3], suggest[4])
            delete_img(suggest[0])
            suggest = next(data, 0)
            if suggest == 0:
                await bot.send_message(call.message.chat.id, 'Предложения закончились')
                return
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('Одобрить', callback_data='confirm'),
                       InlineKeyboardButton('Отклонить', callback_data='decline'))
            with open(f'suggested_locations/{suggest[0]}.jpeg', 'rb') as photo:
                await bot.send_photo(call.message.chat.id, photo,
                                     caption=f'Название: {suggest[2]}\nКоординаты: {suggest[3], suggest[4]}\nПредложил: {print_name(suggest[1])}',
                                     reply_markup=markup)
        elif call.data == 'decline':
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            os.remove(f'suggested_locations/{suggest[0]}.jpeg')
            delete_img(suggest[0])
            suggest = next(data, 0)
            if suggest == 0:
                await bot.send_message(call.message.chat.id, 'Предложения закончились')
                return
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('Одобрить', callback_data='confirm'),
                       InlineKeyboardButton('Отклонить', callback_data='decline'))
            with open(f'suggested_locations/{suggest[0]}.jpeg', 'rb') as photo:
                await bot.send_photo(call.message.chat.id, photo,
                                     caption=f'Название: {suggest[2]}\nКоординаты: {suggest[3], suggest[4]}\nПредложил: {print_name(suggest[1])}',
                                     reply_markup=markup)
        elif call.data == 'online_call':
            await online_mode(call.message)
        elif call.data == 'admin_panel':
            temp_data = get_all()

            def generator(temp_data):
                for i in temp_data:
                    yield i

            data = generator(temp_data)
            suggest = next(data, 0)
            if suggest == 0:
                await bot.send_message(call.message.chat.id, 'Предложений нет')
                return
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('Одобрить', callback_data='confirm'),
                       InlineKeyboardButton('Отклонить', callback_data='decline'))
            with open(f'suggested_locations/{suggest[0]}.jpeg', 'rb') as photo:
                await bot.send_photo(call.message.chat.id, photo,
                                     caption=f'Название: {suggest[2]}\nКоординаты: {suggest[3], suggest[4]}\nПредложил: {print_name(suggest[1])}',
                                     reply_markup=markup)


    @bot.message_handler(content_types=['location'])
    async def fgh_message(message):
        print('loc')
        if not print_curr_img(message.chat.id)[0]:
            await bot.send_message(message.chat.id, 'Cначала нажми кнопку /start и выбери режим')
            return
        markup = InlineKeyboardMarkup()
        if print_pair(message.chat.id) == 0:
            markup.add(InlineKeyboardButton('Назад', callback_data='play'),
                       InlineKeyboardButton('Продолжить', callback_data='classic_mode'))
        msg = tuple([message.location.latitude, message.location.longitude])
        name = [i for i in
                ''.join(print_curr_img(message.chat.id)).replace('images/', '').replace('.jpeg', '').split(', ')]
        name = search_by_id(name[0])
        print(*name, *msg,444)
        answer = list(getDistance(*name, *msg))
        if print_time_bool(message.chat.id):
            if answer[0] == 0:
                answer[0] = -5
            answer[0] *= 2
        await bot.send_photo(message.chat.id, check(name, msg),
                             caption=f'Ты получил баллов: {answer[0]}. \n{answer[1]} - {search_by_coords(*name)[0]}',
                             reply_markup=markup)
        if print_pair(message.chat.id) != 0:
            await online_mode(message)
        else:
            update_curr_img(message.chat.id, None)
        update_score(message.chat.id, answer[0])



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
        try:
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
                update_suggest_stage(message.chat.id, 0)
                await bot.send_message(message.chat.id, '😘')
                await start_message(message)
        except IndexError:
            await bot.send_message(message.chat.id, 'чет не верно')


    async def game_mods(message):
        text = 'Отлично! Выбери режим игры😉'
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton('Обычный', callback_data='classic_mode'),
                   InlineKeyboardButton('На время', callback_data='time_mode'),
                   InlineKeyboardButton('Онлайн', callback_data='online_mode'))
        markup.row(InlineKeyboardButton('назад', callback_data='back1'))
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


    async def online_timer(id):
        await asyncio.sleep(5)
        print(print_pair(id), 123)
        if print_pair(id) == 0:
            await bot.send_message(id, 'Я никого не нашел')
            return True
        update_search(id, 0)
        return True


    async def online_search(event, message):
        while not event.is_set():
            players = print_ready()
            if message.chat.id not in players:
                break
            clear_pair(message.chat.id)
            if len(players) >= 2:
                for i in players:
                    if i != message.chat.id:
                        update_pair(message.chat.id, i)
                        update_search(i, 0)
                        update_search(message.chat.id, 0)
                        await bot.send_message(message.chat.id, f'Я нашел игрока! {i}')
                        await bot.send_message(i, f'Я нашел игрока!{message.chat.id}')
                        update_online_imgs(message.chat.id, 0)
                        update_online_imgs(i, 0)
                        await getimages_online(message, i)
                        break
            await asyncio.sleep(0)
            if event.is_set():
                await asyncio.sleep(0)
                break

    async def getimages_online(message, id_enemy):
        update_online_imgs(message.chat.id, 0)
        update_online_imgs(id_enemy, 0)
        data = getImages(7)
        update_online_imgs(message.chat.id, ':'.join(data))
        update_online_imgs(id_enemy, ':'.join(data))
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Продолжить', callback_data='online_call'))
        await bot.send_message(message.chat.id, f'Твоя задача отгадать 7 картинок быстрее, чем твой соперник!', reply_markup=markup)
        await bot.send_message(id_enemy, f'Твоя задача отгадать 7 картинок быстрее, чем твой соперник!', reply_markup=markup)

    async def online_mode(message):
        print(type(message))
        temp_data = print_online_imgs(message.chat.id).split(':')
        photo = print_online_imgs(message.chat.id).split(':')[0]
        print(photo, temp_data)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Вернуться назад', callback_data='play'))
        update_curr_img(message.chat.id, photo)
        await bot.send_photo(message.chat.id, open(photo, 'rb'), caption='Отправь мне координаты этого места',
                            reply_markup=markup)
        if len(temp_data) > 1:
            update_online_imgs(message.chat.id, ':'.join(temp_data[1:]))
        else:
            pass
            # await end_online_mode

asyncio.run(bot.polling())
