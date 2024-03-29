# Код для помощника

import aiogram as a

import Stickers
import keyboards as k
from main import dp, BotDB
from aiogram import types
from aiogram.dispatcher.filters import Text
from difflib import SequenceMatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from pars_html_bs4 import pars_schedule


class Search(StatesGroup):
    text = State()


class Schedule(StatesGroup):
    step1 = State()


def similar(a_word, b_word):
    return SequenceMatcher(None, a_word, b_word).ratio()


@dp.message_handler(lambda message: message.text == "💬 Помощник", state=None)
async def send(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    status = BotDB.cursor.execute("SELECT status FROM users WHERE user_id = ?", (int(mess.from_user.id),)).fetchone()[0]
    if status == 'ban':
        await mess.bot.send_message(mess.from_user.id, "Вы забанены!")
    else:
        stud_status = BotDB.cursor.execute("SELECT stud_status FROM users WHERE user_id = ?",
                            (int(mess.from_user.id),)).fetchone()[0]
        if stud_status == 'stud':
            await mess.bot.send_message(mess.from_user.id, 'Выберите действие',
                                        reply_markup=k.helper_main_sections_keyboard)
        elif stud_status == 'staff':
            await mess.bot.send_message(mess.from_user.id, 'Выберите действие',
                                        reply_markup=k.helper_main_sections_stuff_keyboard)


@dp.message_handler(lambda message: message.text == "📖 Разделы", state=None)
async def send(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    status = \
    BotDB.cursor.execute("SELECT stud_status FROM users WHERE user_id = ?", (int(mess.from_user.id),)).fetchone()[0]
    if status == 'stud':
        await mess.bot.send_message(mess.from_user.id, 'Выберите раздел',
                                    reply_markup=k.informational_sections_keyboard)
    elif status == 'staff':
        await mess.bot.send_message(mess.from_user.id, 'Выберите раздел',
                                    reply_markup=k.sections_staff_keyboard)


# Разделы и вопросы для студентов
@dp.message_handler(lambda message: message.text in BotDB.get_sections(), state=None)
async def send(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    inline_questions = types.InlineKeyboardMarkup()
    answers = BotDB.get_answers(mess.text)
    for ans in answers:
        inline_questions.add(types.InlineKeyboardButton(text=ans[1], callback_data="answer_" + str(ans[0])))
    await mess.bot.send_message(mess.from_user.id, "Выберите интересующий вас вопрос:", reply_markup=inline_questions)


# Разделы и вопросы для сотрудников
@dp.message_handler(lambda message: message.text in BotDB.get_employee_sections(), state=None)
async def send(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    inline_questions = types.InlineKeyboardMarkup()
    answers = BotDB.get_staff_answers(mess.text)
    for ans in answers:
        inline_questions.add(types.InlineKeyboardButton(text=ans[1], callback_data="answer_" + str(ans[0])))
    await mess.bot.send_message(mess.from_user.id, "Выберите интересующий вас вопрос:", reply_markup=inline_questions)


# Ответ
@dp.callback_query_handler(Text(startswith='answer_'))
async def send_answer(callback_query: types.CallbackQuery):
    answer_id = int(callback_query.data.split('_')[1])
    if BotDB.get_user_stud(callback_query.from_user.id) == 'stud':
        answer_text = BotDB.cursor.execute("SELECT text FROM information WHERE id = ?", (answer_id,)).fetchone()[0] + "\n"
        if BotDB.cursor.execute("SELECT links FROM information WHERE id = ?", (answer_id,)).fetchone()[0] is not None:
            for link in BotDB.cursor.execute("SELECT links FROM information WHERE id = ?", (answer_id,)).fetchone()[0].split(';'):
                answer_text += "\n" + link
        # await callback_query.bot.send_message(callback_query.from_user.id, answer_id)
    else:
        answer_text = BotDB.cursor.execute("SELECT text FROM employee_info WHERE id = ?", (answer_id,)).fetchone()[0] + "\n"
        if BotDB.cursor.execute("SELECT links FROM employee_info WHERE id = ?", (answer_id,)).fetchone()[0] is not None:
            for link in BotDB.cursor.execute("SELECT links FROM employee_info WHERE id = ?", (answer_id,)).fetchone()[0].split(';'):
                answer_text += "\n" + link

    album = types.MediaGroup()
    try:
        images_id = []
        if BotDB.get_user_stud(callback_query.from_user.id) == 'stud' \
                and BotDB.cursor.execute("SELECT image_id FROM information WHERE id = ?", (answer_id,)).fetchone()[0] is not None:
            images_id = BotDB.cursor.execute("SELECT image_id FROM information WHERE id = ?", (answer_id,))\
                .fetchone()[0].split(';')

        elif BotDB.get_user_stud(callback_query.from_user.id) == 'staff' and BotDB.cursor.execute("SELECT image_id FROM employee_info WHERE id = ?", (answer_id,)).fetchone()[0] is not None:
            images_id = BotDB.cursor.execute("SELECT image_id FROM employee_info WHERE id = ?", (answer_id,)).fetchone()[0].split(';')

        if images_id:
            for i in range(len(images_id)):
                if i == (len(images_id) - 1):
                    album.attach_photo(photo=images_id[i], caption=answer_text)
                else:
                    album.attach_photo(photo=images_id[i])
            await callback_query.bot.send_media_group(chat_id=callback_query.from_user.id, media=album)
        else:
            if BotDB.cursor.execute("SELECT buttons FROM information WHERE id = ?", (answer_id,)).fetchone()[0] is not None:
                await callback_query.bot.send_message(callback_query.from_user.id, answer_text)
            else:
                raise Exception("Нет информации")

        # дополнительные кнопки
        if BotDB.get_user_stud(callback_query.from_user.id) == 'stud':
            if BotDB.cursor.execute("SELECT buttons FROM information WHERE id = ?", (answer_id,)).fetchone()[0] is not None:

                buttons_id = list(map(int, BotDB.cursor.execute("SELECT buttons FROM information WHERE id = ?",
                                                                (answer_id,)).fetchone()[0].split(';')))

                buttons_names = []
                for id in buttons_id:
                    buttons_names.append(
                        BotDB.cursor.execute("SELECT text FROM information WHERE id = ?", (id,)).fetchone()[0])

                inline_questions = types.InlineKeyboardMarkup()
                for i in range(len(buttons_id)):
                    inline_questions.add(
                        types.InlineKeyboardButton(text=buttons_names[i], callback_data="answer_" + str(buttons_id[i])))

                await callback_query.bot.send_message(callback_query.from_user.id, "Связанное:",
                                                      reply_markup=inline_questions)
        else:
            if BotDB.cursor.execute("SELECT buttons FROM employee_info WHERE id = ?", (answer_id,)).fetchone()[0] is not None:

                buttons_id = list(map(int, BotDB.cursor.execute("SELECT buttons FROM employee_info WHERE id = ?",
                                                                (answer_id,)).fetchone()[0].split(';')))

                buttons_names = []
                for id in buttons_id:
                    buttons_names.append(
                        BotDB.cursor.execute("SELECT text FROM employee_info WHERE id = ?", (id,)).fetchone()[0])

                inline_questions = types.InlineKeyboardMarkup()
                for i in range(len(buttons_id)):
                    inline_questions.add(
                        types.InlineKeyboardButton(text=buttons_names[i], callback_data="answer_" + str(buttons_id[i])))

                await callback_query.bot.send_message(callback_query.from_user.id, "Связанное:",
                                                      reply_markup=inline_questions)

    except Exception as e:
        await callback_query.message.answer("Информации пока нет")
        await callback_query.message.answer(e)
        await callback_query.bot.send_sticker(callback_query.from_user.id, sticker=Stickers.question)

    await callback_query.answer()


# Поиск
@dp.message_handler(lambda message: message.text == "🔎 Поиск", state=None)
async def send(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    await mess.bot.send_message(mess.from_user.id, 'Введите текст для поиска', reply_markup=k.search_back_keyboard)
    await Search.text.set()


# Обработка поиска
@dp.message_handler(state=Search.text)
async def search(mess: types.Message, state: FSMContext):
    # await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    if mess.text == "↩ Выйти из поиска":
        status = \
            BotDB.cursor.execute("SELECT stud_status FROM users WHERE user_id = ?",
                                 (int(mess.from_user.id),)).fetchone()[0]
        if status == 'stud':
            await mess.bot.send_message(mess.from_user.id, 'Выберите действие',
                                        reply_markup=k.helper_main_sections_keyboard)
        else:
            await mess.bot.send_message(mess.from_user.id, 'Выберите действие',
                                        reply_markup=k.helper_main_sections_stuff_keyboard)
        await state.finish()
    else:
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
            if (len(user_words) <= 2) and (kolvo >= 1):
                keyboard.add(types.InlineKeyboardButton(text=i[2], callback_data="answer_" + str(i[0])))
            elif (len(user_words) >= 3) and (kolvo >= len(i[1]) // 2):
                keyboard.add(types.InlineKeyboardButton(text=i[2], callback_data="answer_" + str(i[0])))
            kolvo = 0
        if len(keyboard["inline_keyboard"]) == 0:
            await mess.bot.send_message(mess.from_user.id, 'Извините, я не смог ничего найти :(')
            await mess.bot.send_sticker(mess.from_user.id, sticker=Stickers.sad)
            await state.finish()
            await mess.bot.send_message(mess.from_user.id, 'Введите текст для поиска',
                                        reply_markup=k.search_back_keyboard)
            await Search.text.set()
        else:
            await mess.bot.send_message(mess.from_user.id, 'Все что я смог найти:', reply_markup=keyboard)
            await mess.bot.send_message(mess.from_user.id, 'Выберите действие',
                                        reply_markup=k.helper_main_sections_keyboard)
            await state.finish()


@dp.message_handler(lambda message: message.text == "📚 Расписание", state=None)
async def schedule(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    await mess.bot.send_message(mess.from_user.id, 'Введите номер группы', reply_markup=k.search_back_keyboard)
    await Schedule.step1.set()


@dp.message_handler(state=Schedule.step1)
async def get_schedule(mess: a.types.Message, state=FSMContext):
    item = mess.text
    await mess.bot.send_message(mess.from_user.id, pars_schedule(item), reply_markup=k.helper_main_sections_keyboard)
    await state.finish()


@dp.message_handler(lambda message: message.text == "↩ Назад")
async def send(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    status = \
        BotDB.cursor.execute("SELECT stud_status FROM users WHERE user_id = ?", (int(mess.from_user.id),)).fetchone()[0]
    if status == 'stud':
        await mess.bot.send_message(mess.from_user.id, 'Выберите действие',
                                    reply_markup=k.helper_main_sections_keyboard)
    else:
        await mess.bot.send_message(mess.from_user.id, 'Выберите действие',
                                    reply_markup=k.helper_main_sections_stuff_keyboard)


@dp.message_handler(lambda message: message.text == "↩ Выйти из поиска")
async def send(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    status = \
        BotDB.cursor.execute("SELECT stud_status FROM users WHERE user_id = ?", (int(mess.from_user.id),)).fetchone()[0]
    if status == 'stud':
        await mess.bot.send_message(mess.from_user.id, 'Выберите действие',
                                    reply_markup=k.helper_main_sections_keyboard)
    else:
        await mess.bot.send_message(mess.from_user.id, 'Выберите действие',
                                    reply_markup=k.helper_main_sections_stuff_keyboard)


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def send_photo_file_id(mess: a.types.Message):
    await mess.reply(mess.photo[-1].file_id)
