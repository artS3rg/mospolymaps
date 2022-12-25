import config as cfg
import aiogram as a
import logging
import keyboards as k
from db import BotDB
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = a.Bot(token=cfg.TOKEN, parse_mode="HTML")
BotDB = BotDB('db.db')
dp = a.Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
start_mess = 'Приветствую тебя, пользователь!\nЭто неофициальный бот Московского Политеха, который поможет тебе не ' \
             'потеряться в 4 стенах :)\nТакже не забудь подписаться на группу Московского Политеха: \nt.me/mospolytech '


@dp.message_handler(commands='start')
async def start(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    if not (BotDB.user_exists(mess.from_user.id)):
        BotDB.add_user(mess.from_user.id, mess.from_user.full_name)
        await mess.bot.send_message(mess.from_user.id, start_mess, reply_markup=k.start_keyboard)
    else:
        status = BotDB.cursor.execute("SELECT status FROM users WHERE user_id = ?", (int(mess.from_user.id),)).fetchone()[0]
        if status == 'ban':
            await mess.bot.send_message(mess.from_user.id, "Вы забанены!")
        else:
            await mess.bot.send_message(mess.from_user.id, 'Добро пожаловать!', reply_markup=k.start_keyboard)


@dp.message_handler(lambda message: message.text == "🗺 Навигатор")
async def navigation(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    status = BotDB.cursor.execute("SELECT status FROM users WHERE user_id = ?", (int(mess.from_user.id),)).fetchone()[0]
    if status == 'ban':
        await mess.bot.send_message(mess.from_user.id, "Вы забанены!")
    else:
        await mess.bot.send_message(mess.from_user.id, 'Выберите корпус', reply_markup=k.navigation_keyboard)


@dp.message_handler(lambda message: message.text == "🏠 Главная")
async def back_home(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    await mess.bot.send_message(mess.from_user.id, 'Главный раздел', reply_markup=k.start_keyboard)


if __name__ == "__main__":
    from handlers import dp

    a.executor.start_polling(dp, skip_updates=False)
