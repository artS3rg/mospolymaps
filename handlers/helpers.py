# Код для помощника

import aiogram as a
import keyboards as k
import os
from main import dp, BotDB
from aiogram import types
from aiogram.dispatcher.filters import Text
from difflib import SequenceMatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


class Search(StatesGroup):
    text = State()


def similar(a_word, b_word):
    return SequenceMatcher(None, a_word, b_word).ratio()


@dp.message_handler(lambda message: message.text == "💬 Помощник", state=None)
async def send(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    status = BotDB.cursor.execute("SELECT status FROM users WHERE user_id = ?", (int(mess.from_user.id),)).fetchone()[0]
    if status == 'ban':
        await mess.bot.send_message(mess.from_user.id, "Вы забанены!")
    else:
        await mess.bot.send_message(mess.from_user.id, 'Выберите действие',
                                    reply_markup=k.helper_main_sections_keyboard)


@dp.message_handler(lambda message: message.text == "📖 Разделы", state=None)
async def send(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    await mess.bot.send_message(mess.from_user.id, 'Выберите раздел', reply_markup=k.informational_sections_keyboard)


# Разделы и вопросы
@dp.message_handler(lambda message: message.text in BotDB.get_sections(), state=None)
async def send(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    inline_questions = types.InlineKeyboardMarkup()
    answers = BotDB.get_answers(mess.text)
    for ans in answers:
        inline_questions.add(types.InlineKeyboardButton(text=ans[1], callback_data="answer_" + str(ans[0])))
    await mess.bot.send_message(mess.from_user.id, "Выберите интересующий вас вопрос:", reply_markup=inline_questions)


# Ответ
@dp.callback_query_handler(Text(startswith='answer_'))
async def send_answer(callback_query: types.CallbackQuery):
    answer_id = int(callback_query.data.split('_')[1])
    answer_text = BotDB.cursor.execute("SELECT text FROM information WHERE id = ?", (answer_id,)).fetchone()[0]

    album = types.MediaGroup()

    try:
        images_id = BotDB.cursor.execute("SELECT image_id FROM information WHERE id = ?", (answer_id,)).fetchone()[
            0].split(';')
        for i in range(len(images_id)):
            if i == (len(images_id) - 1):
                album.attach_photo(photo=images_id[i], caption=answer_text)
            else:
                album.attach_photo(photo=images_id[i])
        await callback_query.bot.send_media_group(chat_id=callback_query.from_user.id, media=album)

    except Exception:
        await callback_query.message.answer("Информации пока нет")

    await callback_query.answer()


# Поиск
@dp.message_handler(lambda message: message.text == "🔎 Поиск", state=None)
async def send(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    await mess.bot.send_message(mess.from_user.id, 'Введите текст для поиска')
    await Search.text.set()


@dp.message_handler(state=Search.text)
async def search(mess: types.Message, state: FSMContext):
    tags = BotDB.cursor.execute("SELECT id, tags, text FROM information").fetchall()
    new_tags = []
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    text = mess.text
    text = text.lower()
    text = text.replace("?", "", 1)
    text = text.replace("как ", "", 1)
    user_words = text.split(' ')
    kolvo = 0
    for i in range(len(tags)):
        new_tags.append([tags[i][0], tags[i][1], tags[i][2]])
    for i in range(len(new_tags)):
        new_tags[i][1] = new_tags[i][1].split(';')
    for i in new_tags:
        if len(keyboard["inline_keyboard"]) == 3:
            break
        for u_word in user_words:
            for j in i[1]:
                if similar(j, u_word) >= 0.7:  # процент при котором слова можно считать схожими
                    kolvo += 1
                    continue
        if (kolvo / len(user_words)) >= 0.5:  # процент при котором кнопка доб в клавиатуру
            keyboard.add(types.InlineKeyboardButton(text=i[2], callback_data="answer_" + str(i[0])))
        kolvo = 0
    if len(keyboard["inline_keyboard"]) == 0:
        await mess.bot.send_message(mess.from_user.id, 'Извините, я не смог ничего найти :(')
    else:
        await mess.bot.send_message(mess.from_user.id, 'Все что я смог найти:', reply_markup=keyboard)
    await state.finish()


@dp.message_handler(lambda message: message.text == "↩ Назад")
async def send(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    await mess.bot.send_message(mess.from_user.id, 'Выберите действие', reply_markup=k.helper_main_sections_keyboard)


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def send_photo_file_id(mess: a.types.Message):
    await mess.reply(mess.photo[-1].file_id)
