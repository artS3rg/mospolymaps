from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import config
import config as cfg
import aiogram as a
import logging
import keyboards as k
from db import BotDB
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types

bot = a.Bot(token=cfg.TOKEN, parse_mode="HTML")
BotDB = BotDB('db.db')
dp = a.Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
start_mess = 'Приветствую тебя, пользователь!\nЭто неофициальный бот Московского Политеха, который поможет тебе не ' \
             'потеряться в 4 стенах :)\nТакже не забудь подписаться на группу Московского Политеха: \nt.me/mospolytech '
next_id = 0


class StaffLog(StatesGroup):
    log_token = State()


@dp.message_handler(commands='start')
async def start(mess: a.types.Message, next_id=next_id):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    if not (BotDB.user_exists(mess.from_user.id)):
        buttons = [
            types.InlineKeyboardButton(text="Войти как студент", callback_data="start_stud"),
            types.InlineKeyboardButton(text="Войти как сотрудник", callback_data="start_staff"),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await mess.bot.send_message(mess.from_user.id, 'Выберите способ входа', reply_markup=keyboard)
        if next_id != 0:
            next_id = mess.message_id + 1
        else:
            next_id = 0
    else:
        status = \
            BotDB.cursor.execute("SELECT status FROM users WHERE user_id = ?", (int(mess.from_user.id),)).fetchone()[0]
        if status == 'ban':
            await mess.bot.send_message(mess.from_user.id, "Вы забанены!")
        else:
            if BotDB.get_user_stud(mess.from_user.id) == 'stud':
                await mess.bot.send_message(mess.from_user.id, 'Добро пожаловать!', reply_markup=k.start_stud_keyboard)
            else:
                await mess.bot.send_message(mess.from_user.id, 'Добро пожаловать!', reply_markup=k.start_staff_keyboard)


@dp.callback_query_handler(text='start_stud', state=None)
async def start_stud(call: a.types.CallbackQuery):
    await call.message.delete()
    await call.bot.send_message(call.from_user.id, 'Добро пожаловать!', reply_markup=k.start_stud_keyboard)
    BotDB.add_user(call.from_user.id, call.from_user.full_name, 'stud')
    buttons = [
        types.InlineKeyboardButton(text="Важная информация!", callback_data="start_info"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await call.bot.send_message(call.from_user.id, start_mess, reply_markup=keyboard)


@dp.callback_query_handler(text='start_staff', state=None)
async def start_staff(call: a.types.CallbackQuery):
    await call.message.delete()
    await call.bot.send_message(call.from_user.id, 'Введите токен для входа')
    await StaffLog.log_token.set()


@dp.message_handler(state=StaffLog.log_token)
async def start_staff_log(mess: a.types.Message, state: FSMContext):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    if mess.text == config.stud_token:
        await mess.bot.send_message(mess.from_user.id, start_mess)
        await mess.bot.send_message(mess.from_user.id, 'Добро пожаловать!', reply_markup=k.start_staff_keyboard)
        BotDB.add_user(mess.from_user.id, mess.from_user.full_name, 'staff')
    else:
        buttons = [
            types.InlineKeyboardButton(text="Войти как студент", callback_data="start_stud"),
            types.InlineKeyboardButton(text="Войти как сотрудник", callback_data="start_staff"),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await mess.bot.send_message(mess.from_user.id, 'Неверный токен!\nВыберите способ входа', reply_markup=keyboard)
    await state.finish()


@dp.message_handler(lambda message: message.text == "🗺 Навигатор")
async def navigation(mess: a.types.Message):
    next_id = mess.message_id + 1
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    status = BotDB.cursor.execute("SELECT status FROM users WHERE user_id = ?", (int(mess.from_user.id),)).fetchone()[0]
    if status == 'ban':
        await mess.bot.send_message(mess.from_user.id, "Вы забанены!")
    else:
        await mess.bot.send_message(mess.from_user.id, 'Выберите корпус', reply_markup=k.navigation_keyboard)


@dp.message_handler(lambda message: message.text == "🏠 Главная")
async def back_home(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    await mess.bot.send_message(mess.from_user.id, 'Главный раздел', reply_markup=k.start_stud_keyboard)


@dp.callback_query_handler(text='start_info', state=None)
async def start_info(call: types.CallbackQuery):
    await call.message.delete()
    media = types.MediaGroup()
    media.attach_photo('AgACAgIAAxkBAAIC4mOfkN7DtCGvUUXAH1wFEIoNrd-mAAKBxDEbyEb5SNKXt3b-tnIpAQADAgADeQADLAQ',
                       'Кружки и секции')
    media.attach_photo('AgACAgIAAxkBAAIC7GOfkUCQs-WRmL4Dj_C6Domk4ftnAAKHxDEbyEb5SDhPm7KZ_-trAQADAgADeQADLAQ',
                       'Психологическая помощь')
    media.attach_photo('AgACAgIAAxkBAAIC7mOfkVpVST3IUVyyzg97ii4FmvKbAAKAxDEbyEb5SLldiansKvs1AQADAgADeQADLAQ',
                       'Фото на пропускс')
    await bot.send_media_group(call.from_user.id, media=media)


if __name__ == "__main__":
    from handlers import dp

    a.executor.start_polling(dp, skip_updates=False)
