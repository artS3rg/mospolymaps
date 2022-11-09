from aiogram import types
from main import dp, BotDB
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


class BsNavigation(StatesGroup):
    bs_point_b_input = State()
    bs_point_b_audit = State()


@dp.message_handler(lambda message: message.text == "Большая Семёновская (БС)", state=None)
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
    text = mess.text
    campus_letters = ["А", "В", "Б", "Н"]
    travel = ""
    if (len(text) != 4) or (text[0] not in campus_letters) or (int(text[1]) > 4):
        await mess.bot.send_message(mess.from_user.id, "Неверная аудитория. Начните заново")
    else:
        travel += "1. Пройдите к аудитории, показанной на карте"
        match text[0]:
            case "А":
                pass
            case "В":
                pass
            case "Б":
                pass
            case "Н":
                pass
    await mess.bot.send_message(mess.from_user.id, travel)
    await state.finish()


@dp.callback_query_handler(text='bs_audit', state=None)
async def bs_marsh_audit(call: types.CallbackQuery):
    pass


@dp.message_handler(state=BsNavigation.bs_point_b_audit)
async def bs_marsh_audit_next(mess: types.Message, state: FSMContext):
    pass
