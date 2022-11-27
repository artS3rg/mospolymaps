# Код для помощника

import aiogram as a
import keyboards as k
from main import dp, BotDB
from aiogram import types
from aiogram.dispatcher.filters import Text


@dp.message_handler(lambda message: message.text == "💬 Помощник", state=None)
async def send(mess: a.types.Message):
    await mess.bot.send_message(mess.from_user.id, 'Выберите действие', reply_markup=k.helper_main_sections_keyboard)


@dp.message_handler(lambda message: message.text == "📖 Разделы", state=None)
async def send(mess: a.types.Message):
    await mess.bot.send_message(mess.from_user.id, 'Выберите раздел', reply_markup=k.informational_sections_keyboard)


# Разделы и вопросы
@dp.message_handler(lambda message: message.text in BotDB.get_sections(), state=None)
async def send(mess: a.types.Message):
    inline_questions = types.InlineKeyboardMarkup()
    answers = BotDB.get_answers(mess.text)
    for ans in answers:
        inline_questions.add(types.InlineKeyboardButton(text=ans[1], callback_data="answer_" + str(ans[0])))
    await mess.bot.send_message(mess.from_user.id, "Выберите интересующий вас вопрос:", reply_markup=inline_questions)


@dp.callback_query_handler(Text(startswith='answer_'))
async def send_answer(callback_query: types.CallbackQuery):
    answer_id = int(callback_query.data.split('_')[1])
    answer_text = BotDB.cursor.execute("SELECT text FROM information WHERE id = ?", (answer_id, )).fetchone()[0]
    await callback_query.message.answer(answer_text)
    await callback_query.answer()


@dp.message_handler(lambda message: message.text == "🔎 Поиск")
async def send(mess: a.types.Message):
    await mess.bot.send_message(mess.from_user.id, 'А его пока нет ┐(￣ヮ￣)┌')


@dp.message_handler(lambda message: message.text == "↩ Назад")
async def send(mess: a.types.Message):
    await mess.bot.send_message(mess.from_user.id, 'Выберите действие', reply_markup=k.helper_main_sections_keyboard)
