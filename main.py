from aiogram import Bot, Dispatcher, executor, types
from book_time import create_new_booking, create_booking_plan
from pytz import timezone
import datetime
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
import sqlalchemy as sa

API_TOKEN = "6513209840:AAE8wC3AqVuaR73-W4EZ_ynmL5fkAbsPO08"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def process_request(request_hour,request_name):
    tz=timezone('Europe/Moscow')
    date_now = datetime.datetime.now(tz)
    if request_hour >= date_now.hour:
        response = create_new_booking(request_hour,request_name,date_now)
    else:
        response = "Час записи должен быть больше текущего времени сегодняшнего дня"

    return response

@dp.message_handler(commands=['start']) #Явно указываем в декораторе, на какую команду реагируем. 
async def send_welcome(message: types.Message):
    hello_message = 'Привет! Я бот для бронирования времени\n'
    hello_message += 'на сервере 192.168.251.133\n'
    hello_message += 'Для бронирования времени напиши свои\n'
    hello_message += 'пожелания в формате "Час, Свое имя"\n'
    hello_message += 'Например, я хочу забронировать сервер с 15 до 16 часов\n'
    hello_message += 'сегодняшнего дня, то я пишу в чате сообщение\n'
    hello_message += '15, Никита Сенчило\n'
    hello_message += '------------------------------------\n'
    hello_message += 'Вспомогательные команды:\n - /start - повторить общую информацию\n - /plan - отобразить график бронирований на сегодня'

    await message.reply(hello_message) #Так как код работает асинхронно, то обязательно пишем await.

@dp.message_handler(commands=['plan']) # Явно указываем в декораторе, на какую команду реагируем. 
async def send_plan(message: types.Message):
    tz=timezone('Europe/Moscow')
    date_now = datetime.datetime.now(tz)
    response = create_booking_plan(date_now)
    await message.reply(response) # Так как код работает асинхронно, то обязательно пишем await.

@dp.message_handler() #Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
async def echo(message: types.Message): #Создаём функцию с простой задачей — отправить обратно тот же текст, что ввёл пользователь.
    request = [i.strip() for i in message.text.split(',')]
    print(request)
    if len(request) == 2:
        try:
            request_hour = int(request[0])
            request_name = request[1]
            response = process_request(request_hour,request_name)
        except:
            response = "Неправильный формат запроса"
    else:
        response = "Неправильный формат запроса"
    await message.answer(response)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)




