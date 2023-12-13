from aiogram import types

import keyboards as k
from main import dp, BotDB
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

pr_info_text = '🔸<b>Адрес учебного корпуса на ул. Прянишникова:</b>\n' \
               '127550, г. Москва, ул. Прянишникова, 2А\n' \
               'Корпуса 1, 2'


class PrNavigation(StatesGroup):
    pr_point_a = State()


@dp.message_handler(lambda message: message.text == "Прянишникова (ПР)", state=None)
async def pr_selected(mess: types.Message):
    await mess.bot.send_message(mess.from_user.id, 'Выберите действие', reply_markup=k.prCampus_keyboard)
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)


@dp.message_handler(lambda message: message.text == "📖 Информация (ПР)", state=None)
async def pr_info(mess: types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    await mess.bot.send_message(mess.from_user.id, pr_info_text)


@dp.message_handler(lambda message: message.text == "🔻 Маршрут (ПР)", state=None)
async def pr_navigation(mess: types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    buttons = [
        types.InlineKeyboardButton(text="📚 Библиотека", callback_data="input_library"),
        types.InlineKeyboardButton(text="🥼 Гардероб", callback_data="input_cloakroom"),
        types.InlineKeyboardButton(text="👕 М Туалет", callback_data="input_m_wc"),
        types.InlineKeyboardButton(text="👚 Ж Туалет", callback_data="input_w_wc"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await mess.bot.send_message(mess.from_user.id, 'Введите номер нужной Вам аудитории\nИли выберите маршрут ниже ⬇️',
                                reply_markup=keyboard)
    await PrNavigation.pr_point_a.set()


@dp.callback_query_handler(text='input_library', state=PrNavigation.pr_point_a)
async def input_library(call: types.CallbackQuery, state: FSMContext):
    photo_id = \
        BotDB.cursor.execute("SELECT photo_id FROM auds_pr_2 WHERE name = ?", ("Библиотека",)).fetchone()[0]
    await call.bot.send_photo(call.from_user.id, photo_id)
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(text='input_m_wc', state=PrNavigation.pr_point_a)
async def input_m_wc(call: types.CallbackQuery, state: FSMContext):
    photo_id = \
        BotDB.cursor.execute("SELECT photo_id FROM auds_pr_2 WHERE name = ?", ("М_Туалет",)).fetchone()[0]
    await call.bot.send_photo(call.from_user.id, photo_id)
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(text='input_w_wc', state=PrNavigation.pr_point_a)
async def input_w_wc(call: types.CallbackQuery, state: FSMContext):
    photo_id = \
        BotDB.cursor.execute("SELECT photo_id FROM auds_pr_2 WHERE name = ?", ("Ж_Туалет",)).fetchone()[0]
    await call.bot.send_photo(call.from_user.id, photo_id)
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(text='input_cloakroom', state=PrNavigation.pr_point_a)
async def input_cloakroom(call: types.CallbackQuery, state: FSMContext):
    photo_id = \
        BotDB.cursor.execute("SELECT photo_id FROM auds_pr_2 WHERE name = ?", ("Гардероб",)).fetchone()[0]
    await call.bot.send_photo(call.from_user.id, photo_id)
    await call.message.delete()
    await state.finish()


@dp.message_handler(state=PrNavigation.pr_point_a)
async def pr_travel(mess: types.Message, state: FSMContext):
    if mess.text == "🔻 Маршрут (ПР)":
        await mess.bot.delete_message(mess.from_user.id, mess.message_id)
        buttons = [
            types.InlineKeyboardButton(text="📚 Библиотека", callback_data="input_library"),
            types.InlineKeyboardButton(text="🥼 Гардероб", callback_data="input_cloakroom"),
            types.InlineKeyboardButton(text="👕 М Туалет", callback_data="input_m_wc"),
            types.InlineKeyboardButton(text="👚 Ж Туалет", callback_data="input_w_wc"),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await mess.bot.send_message(mess.from_user.id,
                                    'Введите номер нужной Вам аудитории\nИли выберите маршрут ниже ⬇️')
        await PrNavigation.pr_point_a.set()
    elif mess.text == "📖 Информация (ПР)":
        await mess.bot.delete_message(mess.from_user.id, mess.message_id)
        await mess.bot.send_message(mess.from_user.id, pr_info_text)
    elif mess.text == "🏠 Главная":
        await mess.bot.send_message(mess.from_user.id, "Выберите действие", reply_markup=k.start_stud_keyboard)
    else:
        photos = BotDB.cursor.execute("SELECT * FROM auds_pr_2 WHERE name = ?", (mess.text,)).fetchall()
        if len(photos) == 0:
            await mess.bot.send_message(mess.from_user.id, "Неверная аудитория. Начните заново ❌")
        elif len(photos) == 1:
            await mess.bot.send_photo(mess.from_user.id, photos[0][2])
        else:
            media = types.MediaGroup()
            for i in photos:
                media.attach_photo(photo=i[2])
            await mess.bot.send_media_group(mess.from_user.id, media)
    await state.finish()
