from aiogram import types
from dispatcher import dp
from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State

import sqlite3
import config
import re
from bot import BotDB

@dp.message_handler(commands = "start")
async def start(message: types.Message):
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id, "Добро пожаловать!")

class ProfileStatesGroup(StatesGroup):

    photo = State()
    name = State()
    age = State()
    description = State()
def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/Otzhimania'))
    return kb


@dp.message_handler(commands=['trainadd'])
async def cmd_profile(message: types.Message) -> None:
    await message.reply('Добавьте упражнение', reply_markup=get_kb())
    await ProfileStatesGroup.photo.set()


@dp.message_handler(commands=['Otzhimania'])
async def cmd_create(message: types.Message,) -> None:
    await message.answer('Упражнение выбрано')
    conn = sqlite3.connect('Train_base.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO `uprazhnenia` (`Nazvanie`) VALUES (?)") #(user_id,))
    conn.commit()
    conn.close()



#def close(self):
    """Закрываем соединение с БД"""
    #self.connection.close()


@dp.message_handler() #для выдачи ошибки при несуществующей команде
async def warning(message: types.Message):
    await message.answer(text=('Не понимаю твою унга-бунгу, напиши / если нужна помощь')) #Написать сообщение