# Код для помощника

import aiogram as a
import keyboards as k
from main import dp


@dp.message_handler(lambda message: message.text == "💬 Помощник", state=None)
async def send(mess: a.types.Message):
    await mess.bot.send_message(mess.from_user.id, 'Выберите действие', reply_markup=k.helper_main_sections_keyboard)


@dp.message_handler(lambda message: message.text == "📖 Разделы", state=None)
async def send(mess: a.types.Message):
    await mess.bot.send_message(mess.from_user.id, 'Выберите раздел', reply_markup=k.informational_sections_keyboard)


@dp.message_handler(lambda message: message.text == "🔎 Поиск")
async def send(mess: a.types.Message):
    await mess.bot.send_message(mess.from_user.id, 'А его пока нет ┐(￣ヮ￣)┌')


@dp.message_handler(lambda message: message.text == "↩ Назад")
async def send(mess: a.types.Message):
    await mess.bot.send_message(mess.from_user.id, 'Выберите действие', reply_markup=k.helper_main_sections_keyboard)
