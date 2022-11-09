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
    if not (BotDB.user_exists(mess.from_user.id)):
        BotDB.add_user(mess.from_user.id, mess.from_user.full_name)
        await mess.bot.send_message(mess.from_user.id, start_mess, reply_markup=k.start_keyboard)
    else:
        await mess.bot.send_message(mess.from_user.id, 'Добро пожаловать!', reply_markup=k.start_keyboard)


@dp.message_handler(lambda message: message.text == "🗺Навигатор")
async def navigation(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    await mess.bot.send_message(mess.from_user.id, 'Выберите корпус', reply_markup=k.navigation_keyboard)


@dp.message_handler(lambda message: message.text == "❓FAQ")
async def info(mess: a.types.Message):
    a = '🔸<b>Адрес кампуса на Большой Семёновской:</b>\n' \
        'учебные корпуса «А», «Б», «В», «Н», «НД»\n' \
        'ст. м. «Электрозаводская» или ж/д станция Электрозаводская, ул. Б. Семёновская, д. 38.\n' \
        '🔸<b>Адрес учебного корпуса на ст. м. «Автозаводская»:</b>\n' \
        '115280, г. Москва, ул. Автозаводская, д. 16 (ст. м. «Автозаводская»)\n' \
        'Проезд:\n' \
        '- от станции метро «Автозаводская» (выход №2) на автобусах 44, 142, т40 до ост. «Парк Легенд», далее пешком ' \
        '2 минуты;\n' \
        '- от станции метро «Автозаводская» (выход №3) на автобусах 9, 99, 186, Т26, Т67 до ост. «Парк Легенд», ' \
        'далее пешком 2 минуты.\n' \
        '🔸<b>Адрес учебного корпуса на ст. м. «ВДНХ»:</b>\n' \
        'ул. Павла Корчагина, д. 22.\n' \
        'Проезд:\n' \
        '- от станции метро «ВДНХ» (выход №4 и №5) на автобусах 378, 286 до ост. «Гимназия», далее пешком меньше 5 ' \
        'минут;\n' \
        '- от станции метро «ВДНХ» (выход №1) на трамваях 11, 25 до ост. «Пл. Академика Люльки», далее пешком 8 ' \
        'минут;\n' \
        '- от станции метро «Алексеевская» пройти до остановки на ул. Мытищинская 3-я пешком 6 минут, ' \
        'сесть на автобус 714 до ост. «Гимназия», далее пешком 3 минуты.\n' \
        '🔸<b>Адрес учебного корпуса на ул. Прянишникова:</b>\n' \
        '127550, г. Москва, ул. Прянишникова, 2А\n' \
        'Корпуса 1, 2\n' \
        'Проезд:\n' \
        '- от станции метро «Петровско-Разумовская» (первая линия остановок от метро), платформы ' \
        '«Петровско-Разумовская» на автобусах 114, 204, 282, т19, 300 до ост. «Кинотеатр «Байкал»» (15–20 минут), ' \
        'далее пешком 8 минут вдоль пруда;\n' \
        '- от станции метро «Войковская» на автобусах 204, 179, 282, 591, 114 до ост. «Михалковская улица» (15–20 ' \
        'минут), далее пешком 8 минут вдоль пруда;\n' \
        '- от станции метро «Дмитровская» на трамвае 29, 27 или «Войковская» на трамвае 27 до ост. «Политехнический ' \
        'университет» (15–20 минут);\n' \
        '- от Савёловского вокзала или станции метро «Савёловская» на автобусах 72, 87 до ост. «Политехнический ' \
        'университет»;\n' \
        '- от станции МЦК «Коптево» на трамвае 27к, автобусах 22, 595, 72, 801, 87 до ост. «Политехнический ' \
        'университет» или пешком 20 минут;\n' \
        '- от платформы «Красный Балтиец» на автобусах т57, т19, 300 до ост. «Михалковская улица», далее пройти назад ' \
        'и идти пешком вдоль пруда 7 минут;\n' \
        '- от станции метро «Селигерская» на автобусах 591, 179 до ост. «Михалковская улица» (15–20 минут), ' \
        'далее пешком 8 минут вдоль пруда.\n '
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    await mess.bot.send_message(mess.from_user.id, a)


@dp.message_handler(lambda message: message.text == "🏠Главная")
async def back_home(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    await mess.bot.send_message(mess.from_user.id, 'Главный раздел', reply_markup=k.start_keyboard)


if __name__ == "__main__":
    from handlers import dp

    a.executor.start_polling(dp, skip_updates=False)
