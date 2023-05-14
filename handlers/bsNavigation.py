from aiogram import types

import keyboards
from main import dp, BotDB
from keyboards import bsCampus_keyboard
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from datetime import datetime


class BsNavigation(StatesGroup):
    bs_point_b_input = State()
    bs_point_b_audit = State()

def navigate(text, forward, min_left, max_left, min_right, max_right, none) -> str:
    def_travel = ''
    if text == forward:
        def_travel += '2. Пройдите вперед ⬆️\n'
    elif text == none:
        def_travel = ''
    else:
        if () or ():
            def_travel += '2. Поверните направо ➡️\n'
        elif (text >= min_left) or (text <= max_left):
            def_travel += '2. Поверните налево ⬅️\n'
        else:
            def_travel = 'error'
    return def_travel

@dp.message_handler(lambda message: message.text == "Большая Семёновская (БС)", state=None)
async def bs_selected(mess: types.Message):
    await mess.bot.send_message(mess.from_user.id, 'Выберите действие', reply_markup=bsCampus_keyboard)
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)


@dp.message_handler(lambda message: message.text == "📖 Информация (БС)", state=None)
async def bs_info(mess: types.Message):
    bs_info_text = '🔸<b>Адрес кампуса на Большой Семёновской:</b>\n' \
                   'учебные корпуса «А», «Б», «В», «Н», «НД»\n' \
                   'ст. м. «Электрозаводская» или ж/д станция Электрозаводская, ул. Б. Семёновская, д. 38.'
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    await mess.bot.send_message(mess.from_user.id, bs_info_text)


@dp.message_handler(lambda message: message.text == "🔻 Маршрут (БС)", state=None)
async def bs_navigation(mess: types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    buttons = [
        types.InlineKeyboardButton(text="Вход", callback_data="bs_input"),
        # types.InlineKeyboardButton(text="Аудитория", callback_data="bs_audit"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await mess.bot.send_message(mess.from_user.id, 'Выберите начало маршрута', reply_markup=keyboard)


@dp.callback_query_handler(text='bs_input', state=None)
async def bs_nav_input(call: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="💊 Медпункт", callback_data="input_med"),
        types.InlineKeyboardButton(text="⚽️ Спортзал", callback_data="input_sport"),
        types.InlineKeyboardButton(text="👕 М Туалет", callback_data="input_m_wc"),
        types.InlineKeyboardButton(text="👚 Ж Туалет", callback_data="input_zh_wc"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await call.message.delete()
    await call.bot.send_message(call.from_user.id, 'Введите номер нужной Вам аудитории\nИли выберите маршрут ниже ⬇️', reply_markup=keyboard)
    await BsNavigation.bs_point_b_input.set()

@dp.callback_query_handler(text='input_med', state=BsNavigation.bs_point_b_input)
async def input_med(call: types.CallbackQuery, state:FSMContext):
    travel = "1. Пройдите налево к лестнице и поднимитесь на 1 этаж ⤴️\n" \
             "2. Поверните налево ⬅️\n" \
             "3. Пройдите вперед ⬆️\n" \
             "4. Пройдите к аудитории, показанной на карте ✅"
    time = int(datetime.now().strftime("%H"))
    if (time > 8) and (time < 20):
        photo_id = BotDB.cursor.execute("SELECT photo_id FROM auds_light_bs_A WHERE name = ?", ("Медпункт1",)).fetchone()[0]
    else:
        photo_id = BotDB.cursor.execute("SELECT photo_id FROM auds_dark_bs_A WHERE name = ?", ("Медпункт1",)).fetchone()[0]
    await call.bot.send_photo(call.from_user.id, photo_id, travel)
    await call.message.delete()
    await state.finish()

@dp.callback_query_handler(text='input_sport', state=BsNavigation.bs_point_b_input)
async def input_med(call: types.CallbackQuery, state:FSMContext):
    travel = "1. Пройдите налево к лестнице и поднимитесь на 1 этаж ⤴️\n" \
             "2. Поверните налево ⬅️\n" \
             "3. Пройдите вперед до правого коридора ⬆️\n" \
             "4. Поверните направо ➡️\n" \
             "5. Пройдите вперед ⬆️\n" \
             "6. Пройдите к аудитории, показанной на карте ✅"
    time = int(datetime.now().strftime("%H"))
    if (time > 8) and (time < 20):
        photo_id = BotDB.cursor.execute("SELECT photo_id FROM auds_light_bs_A WHERE name = ?", ("Спортзал1",)).fetchone()[0]
    else:
        photo_id = BotDB.cursor.execute("SELECT photo_id FROM auds_dark_bs_A WHERE name = ?", ("Спортзал1",)).fetchone()[0]
    await call.bot.send_photo(call.from_user.id, photo_id, travel)
    await call.message.delete()
    await state.finish()

@dp.callback_query_handler(text='input_m_wc', state=BsNavigation.bs_point_b_input)
async def input_med(call: types.CallbackQuery, state:FSMContext):
    travel = "1. Пройдите налево к лестнице и поднимитесь на 1 этаж ⤴️\n" \
             "2. Поверните направо ➡️\n" \
             "3. Пройдите вперед до упора ⬆️\n" \
             "4. Поверните налево ⬅️\n" \
             "5. Пройдите вперед ⬆️\n" \
             "6. Пройдите к аудитории, показанной на карте ✅"
    time = int(datetime.now().strftime("%H"))
    if (time > 8) and (time < 20):
        photo_id = \
        BotDB.cursor.execute("SELECT photo_id FROM auds_light_bs_A WHERE name = ?", ("МТуалет1",)).fetchone()[0]
    else:
        photo_id = \
        BotDB.cursor.execute("SELECT photo_id FROM auds_dark_bs_A WHERE name = ?", ("МТуалет1",)).fetchone()[0]
    await call.bot.send_photo(call.from_user.id, photo_id, travel)
    await call.message.delete()
    await state.finish()

@dp.callback_query_handler(text='input_zh_wc', state=BsNavigation.bs_point_b_input)
async def input_med(call: types.CallbackQuery, state:FSMContext):
    travel = "1. Пройдите налево к лестнице и поднимитесь на 1 этаж ⤴️\n" \
             "2. Поверните налево ⬅️\n" \
             "3. Пройдите к аудитории, показанной на карте ✅"
    time = int(datetime.now().strftime("%H"))
    if (time > 8) and (time < 20):
        photo_id = \
        BotDB.cursor.execute("SELECT photo_id FROM auds_light_bs_A WHERE name = ?", ("ЖТуалет1",)).fetchone()[0]
    else:
        photo_id = \
        BotDB.cursor.execute("SELECT photo_id FROM auds_dark_bs_A WHERE name = ?", ("ЖТуалет1",)).fetchone()[0]
    await call.bot.send_photo(call.from_user.id, photo_id, travel)
    await call.message.delete()
    await state.finish()

@dp.message_handler(state=BsNavigation.bs_point_b_input)
async def bs_nav_input_next(mess: types.Message, state: FSMContext):
    if mess.text == "🔻 Маршрут (БС)":
        await mess.bot.delete_message(mess.from_user.id, mess.message_id)
        buttons = [
            types.InlineKeyboardButton(text="Вход", callback_data="bs_input"),
            # types.InlineKeyboardButton(text="Аудитория", callback_data="bs_audit"),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await mess.bot.send_message(mess.from_user.id, 'Выберите начало маршрута', reply_markup=keyboard)
    elif mess.text == "📖 Информация (БС)":
        bs_info_text = '🔸<b>Адрес кампуса на Большой Семёновской:</b>\n' \
                       'учебные корпуса «А», «Б», «В», «Н», «НД»\n' \
                       'ст. м. «Электрозаводская» или ж/д станция Электрозаводская, ул. Б. Семёновская, д. 38.'
        await mess.bot.delete_message(mess.from_user.id, mess.message_id)
        await mess.bot.send_message(mess.from_user.id, bs_info_text)
    elif mess.text == "🏠 Главная":
        await mess.bot.send_message(mess.from_user.id, "Выберите действие", reply_markup=keyboards.start_keyboard)
    else:
        k = 3
        text = mess.text
        campus_letters = ["А", "В", "Б", "Н"]
        text = text.replace("A", "А", 1)
        text = text.replace("B", "В", 1)
        text = text.replace("H", "Н", 1)
        travel = ""
    await state.finish()


@dp.callback_query_handler(text='bs_audit', state=None)
async def bs_marsh_audit(call: types.CallbackQuery):
    await call.message.delete()
    await call.bot.send_message(call.from_user.id, 'Введите номер нужной Вам аудитории')
    await BsNavigation.bs_point_b_audit.set()


@dp.message_handler(state=BsNavigation.bs_point_b_audit)
async def bs_marsh_audit_next(state: FSMContext):
    await state.finish()
