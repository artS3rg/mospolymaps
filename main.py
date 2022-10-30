import config as cfg
import aiogram as a
# from aiogram.utils.emoji import emojize
import logging
from db import BotDB
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = a.Bot(token=cfg.TOKEN, parse_mode="HTML")
BotDB = BotDB('db.db')
dp = a.Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

admin_id = 575770908
start_mess = 'Приветствую тебя, пользователь!\nЭто неофициальный бот Московского Политеха, который поможет тебе не' \
             'потеряться в 4 стенах :)\nТакже не забудь подписаться на канал Московского Политеха: \nt.me/mospolytech'


class NewIdea(StatesGroup):
    text = State()


class Marshrut(StatesGroup):
    point_a = State()
    point_b = State()


class Pr_marshrut(StatesGroup):
    pr_point_b = State()


class Bs_marshrut(StatesGroup):
    bs_point_b_vhod = State()
    bs_point_b_audit = State()


start_buttons = ["🔻Маршрут", "📖Полезная информация", "🆕Предложить идею"]
start_keyboard = a.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
start_keyboard.add(*start_buttons)

marshrut_buttons = ["Большая Семёновская (БС)", "↪️Назад"]
marshrut_keyboard = a.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
marshrut_keyboard.add(*marshrut_buttons)


@dp.message_handler(commands='start')
async def start(mess: a.types.Message):
    if not (BotDB.user_exists(mess.from_user.id)):
        BotDB.add_user(mess.from_user.id, mess.from_user.full_name)
        await mess.bot.send_message(mess.from_user.id, start_mess, reply_markup=start_keyboard)
    else:
        await mess.bot.send_message(mess.from_user.id, 'Добро пожаловать!', reply_markup=start_keyboard)


@dp.message_handler(lambda message: message.text == "🔻Маршрут")
async def marshrut(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    await mess.bot.send_message(mess.from_user.id, 'Выберите корпус', reply_markup=marshrut_keyboard)


@dp.message_handler(lambda message: message.text == "↪️Назад")
async def back(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    await mess.bot.send_message(mess.from_user.id, 'Главный раздел', reply_markup=start_keyboard)


@dp.message_handler(lambda message: message.text == "📖Полезная информация")
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


"""Новая идея"""


@dp.message_handler(lambda message: message.text == "🆕Предложить идею", state=None)
async def new_idea(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    ideas = BotDB.cursor.execute("SELECT * FROM `ideas` WHERE `user_id` = ? AND `status` = ?",
                                 (mess.from_user.id, 'wait')).fetchall()
    if len(ideas) == 0:
        await mess.bot.send_message(mess.from_user.id, 'Напишите то, что хотели бы добавить в Нашего бота')
        await NewIdea.text.set()
    else:
        await mess.bot.send_message(mess.from_user.id, "Вашу прошлую идею ещё не рассмотрели!")


@dp.message_handler(state=NewIdea.text)
async def new_idea_text(mess: a.types.Message, state: FSMContext):
    buttons = [
        a.types.InlineKeyboardButton(text="✅Одобрить", callback_data=f"new_idea_yes_{mess.from_user.id}"),
        a.types.InlineKeyboardButton(text="❌Отказать", callback_data=f"new_idea_no_{mess.from_user.id}"),
    ]
    keyboard = a.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    BotDB.add_idea(mess.from_user.id, mess.from_user.full_name, mess.text)
    await mess.bot.send_message(mess.from_user.id, 'Спасибо за Вашу идею!\nСотрудник скоро рассмотрит Ваше предложение')
    await mess.bot.send_message(admin_id, f'Пользователь {mess.from_user.full_name} предложил новую идею!\n{mess.text}',
                                reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(lambda call: call.data.startswith('new_idea_yes_'))
async def new_idea_yes(call: a.types.CallbackQuery):
    id = call.data[13:]
    BotDB.cursor.execute("UPDATE `ideas` SET `status` = ? WHERE `user_id` = ? AND `status` = ?", ('yes', id, 'wait'))
    BotDB.conn.commit()
    await call.bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                             reply_markup=None)
    await call.message.edit_text(f'{call.message.text}\n✅Одобрено')
    await call.bot.send_message(id, 'Вашу идею одобрили!')


@dp.callback_query_handler(lambda call: call.data.startswith('new_idea_no_'))
async def new_idea_no(call: a.types.CallbackQuery):
    id = call.data[12:]
    BotDB.cursor.execute("UPDATE `ideas` SET `status` = ? WHERE `user_id` = ? AND `status` = ?", ('no', id, 'wait'))
    BotDB.conn.commit()
    await call.bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                             reply_markup=None)
    await call.message.edit_text(f'{call.message.text}\n❌Отказано')
    await call.bot.send_message(id, 'Вашу идею отклонили!')


"""Новая идея"""

"""Пряники"""


@dp.message_handler(lambda message: message.text == "Прянишникова (ПР)", state=None)
async def pr_marshrut(mess: a.types.Message):
    buttons = [
        a.types.InlineKeyboardButton(text="Вход", callback_data="pr_vhod"),
        a.types.InlineKeyboardButton(text="Аудитория", callback_data="pr_audit"),
    ]
    keyboard = a.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    await mess.bot.send_message(mess.from_user.id, 'Выберите начало маршрута', reply_markup=keyboard)


@dp.callback_query_handler(text='pr_vhod', state=None)
async def pr_marshrut_vhod(call: a.types.CallbackQuery):
    await call.message.delete()
    await call.bot.send_message(call.from_user.id, 'Введите номер нужной Вам аудитории')
    await Pr_marshrut.pr_point_b.set()


@dp.callback_query_handler(state=Pr_marshrut.pr_point_b)
async def pr_marshrut_vhod_next(mess: a.types.Message, state: FSMContext):
    await state.finish()


@dp.callback_query_handler(text='pr_audit', state=None)
async def pr_marshrut_audit(call: a.types.CallbackQuery):
    await call.message.delete()


"""Пряники"""

"""Автозаводская"""


@dp.message_handler(lambda message: message.text == "Автозаводская (АВ)", state=None)
async def av_marshrut(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)


"""Автозаводская"""

"""Павла Корчагина"""


@dp.message_handler(lambda message: message.text == "Павла Корчагина (ПК)", state=None)
async def pk_marshrut(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)


"""Павла Корчагина"""

"""Большая Семён"""


@dp.message_handler(lambda message: message.text == "Большая Семёновская (БС)", state=None)
async def bs_marshrut(mess: a.types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    buttons = [
        a.types.InlineKeyboardButton(text="Вход", callback_data="bs_vhod"),
        a.types.InlineKeyboardButton(text="Аудитория", callback_data="bs_audit"),
    ]
    keyboard = a.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await mess.bot.send_message(mess.from_user.id, 'Выберите начало маршрута', reply_markup=keyboard)


@dp.callback_query_handler(text='bs_vhod', state=None)
async def bs_marsh_vhod(call: a.types.CallbackQuery):
    await call.message.delete()
    await call.bot.send_message(call.from_user.id, 'Введите номер нужной Вам аудитории')
    await Bs_marshrut.bs_point_b_vhod.set()


@dp.message_handler(state=Bs_marshrut.bs_point_b_vhod)
async def bs_marsh_vhod_next(mess: a.types.Message, state: FSMContext):
    text = mess.text
    campus_letters = ["А", "В", "Б", "Н"]
    travel = ""
    if (len(text) != 4) or (text[0] not in campus_letters) or (int(text[1]) > 4):
        await mess.bot.send_message(mess.from_user.id, "Неверная аудитория. Начните заново")
    else:
        match text[0]:
            case "А":
                pass
            case "В":
                pass
            case "Б":
                pass
            case "Н":
                pass
        travel += "1. Пройдите к аудитории, показанной на карте"
    await mess.bot.send_message(mess.from_user.id, travel)
    await state.finish()


@dp.callback_query_handler(text='bs_audit', state=None)
async def bs_marsh_audit(call: a.types.CallbackQuery):
    pass


@dp.message_handler(state=Bs_marshrut.bs_point_b_audit)
async def bs_marsh_audit_next(mess: a.types.Message, state: FSMContext):
    pass


"""Большая Семён"""

if __name__ == "__main__":
    a.executor.start_polling(dp, skip_updates=False)
