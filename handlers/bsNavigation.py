from aiogram import types
from main import dp, BotDB
from keyboards import bsCampus_keyboard
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


class BsNavigation(StatesGroup):
    bs_point_b_input = State()
    bs_point_b_audit = State()


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
        types.InlineKeyboardButton(text="Аудитория", callback_data="bs_audit"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await mess.bot.send_message(mess.from_user.id, 'Выберите действие', reply_markup=keyboard)


@dp.callback_query_handler(text='bs_input', state=None)
async def bs_nav_input(call: types.CallbackQuery):
    await call.message.delete()
    await call.bot.send_message(call.from_user.id, 'Введите номер нужной Вам аудитории')
    await BsNavigation.bs_point_b_input.set()


@dp.message_handler(state=BsNavigation.bs_point_b_input)
async def bs_nav_input_next(mess: types.Message, state: FSMContext):
    global photo
    text = mess.text
    campus_letters = ["А", "В", "Б", "Н"]
    travel = ""
    if (len(text) != 4) or (text[0] not in campus_letters) or (text[1] in campus_letters) or (text[2] in campus_letters) or (text[3] in campus_letters):
        if (int(text[1]) > 4) or (int(text[2]) > 2):
            await mess.bot.send_message(mess.from_user.id, "Неверная аудитория. Начните заново")
    else:
        match text[0]:
            case "А":
                photo = types.InputFile('C:/Users/ArtSe/OneDrive/Рабочий стол/mospolymaps/auditors_photos/3_level.jpg')
                try:
                    audit = text[1:]
                    k = 1
                    travel += f"{k}. Пройдите налево к лестнице и поднимитесь на {audit[0]} этаж\n"
                    k += 1
                    if audit[0] == '1':
                        pass
                    elif audit[0] == '2':
                        pass
                    elif audit[0] == '3':
                        if audit == '316':
                            travel += f"{k}. Пройдите вперед\n"
                            k += 1
                        else:
                            if (int(audit[1:]) < 16) and (int(audit[1:]) > 0):
                                travel += f"{k}. Поверните налево\n"
                                k += 1
                            elif (int(audit[1:]) > 16) and (int(audit[1:]) < 27):
                                travel += f"{k}. Поверните направо\n"
                                k += 1
                            else:
                                await mess.bot.send_message(mess.from_user.id, "Неверная аудитория. Начните заново")
                                await state.finish()
                    elif audit[0] == '4':
                        if audit == '415':
                            travel += f"{k}. Пройдите вперед\n"
                            k += 1
                        else:
                            if (int(audit[1:]) < 15) and (int(audit[1:]) > 0):
                                travel += f"{k}. Поверните налево\n"
                                k += 1
                            elif (int(audit[1:]) > 15) and (int(audit[1:]) < 26):
                                travel += f"{k}. Поверните направо\n"
                                k += 1
                            else:
                                await mess.bot.send_message(mess.from_user.id, "Неверная аудитория. Начните заново")
                                await state.finish()
                except:
                    await mess.bot.send_message(mess.from_user.id, "Неверная аудитория. Начните заново")
                    await state.finish()
            case "В":
                try:
                    pass
                except:
                    await mess.bot.send_message(mess.from_user.id, "Неверная аудитория. Начните заново")
                    await state.finish()
            case "Б":
                try:
                    pass
                except:
                    await mess.bot.send_message(mess.from_user.id, "Неверная аудитория. Начните заново")
                    await state.finish()
            case "Н":
                try:
                    pass
                except:
                    await mess.bot.send_message(mess.from_user.id, "Неверная аудитория. Начните заново")
                    await state.finish()
        travel += f"{k}. Пройдите к аудитории, показанной на карте"
        await mess.bot.send_photo(mess.from_user.id, photo, travel)
    await state.finish()


@dp.callback_query_handler(text='bs_audit', state=None)
async def bs_marsh_audit(call: types.CallbackQuery):
    await call.message.delete()
    await call.bot.send_message(call.from_user.id, 'Введите номер нужной Вам аудитории')
    await BsNavigation.bs_point_b_audit.set()


@dp.message_handler(state=BsNavigation.bs_point_b_audit)
async def bs_marsh_audit_next(mess: types.Message, state: FSMContext):
    await state.finish()
