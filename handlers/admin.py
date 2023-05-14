from aiogram import types
from main import dp, BotDB
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class NewPost(StatesGroup):
    text = State()

class Ban(StatesGroup):
    ban_id = State()

class NewPoll(StatesGroup):
    sects = State()
    text = State()
    one_sect = State()
    two_sect = State()
    thr_sect = State()
    fou_sect = State()

@dp.message_handler(commands='admin')
async def admin(mess: types.Message):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    status = BotDB.cursor.execute("SELECT status FROM users WHERE user_id = ?", (mess.from_user.id,)).fetchone()[0]
    buttons = [
        types.InlineKeyboardButton(text="Создать пост", callback_data="new_post"),
        types.InlineKeyboardButton(text="Создать опрос", callback_data="new_opros"),
        types.InlineKeyboardButton(text="Забанить", callback_data="ban"),
        types.InlineKeyboardButton(text="Закрыть", callback_data="close"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    if status == 'admin':
        await mess.bot.send_message(mess.from_user.id, "Панель администратора", reply_markup=keyboard)
    else:
        await mess.bot.send_message(mess.from_user.id, "Недостаточно прав!")

#

@dp.callback_query_handler(text="close", state=None)
async def close_panel(call: types.CallbackQuery):
    await call.message.delete()

#

@dp.callback_query_handler(text="new_post", state=None)
async def new_post(call: types.CallbackQuery):
    await call.message.delete()
    await call.bot.send_message(call.from_user.id, "Введите текст сообщения")
    await NewPost.text.set()

@dp.message_handler(state=NewPost.text)
async def new_post_finish(mess: types.Message, state: FSMContext):
    #потом будет и фото
    ids = BotDB.cursor.execute("SELECT user_id FROM users").fetchall()
    for i in ids:
        await mess.bot.send_message(i[0], mess.text)
    await state.finish()

#

#ЕЩЕ ДЕЛАЕТСЯ
@dp.callback_query_handler(text="new_opros", state=None)
async def new_opros(call: types.CallbackQuery):
    await call.message.delete()
    await call.bot.send_message(call.from_user.id, "Введите кол-во ответов (макс. 4)")
    await NewPoll.sects.set()

@dp.message_handler(state=NewPoll.sects)
async def new_opr_sects(mess: types.Message, state:FSMContext):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    sects = int(mess.text)
    if (sects < 1) or (sects > 4):
        pass

#

@dp.callback_query_handler(text="ban", state=None)
async def ban(call: types.CallbackQuery):
    await call.bot.send_message(call.from_user.id, "Введите id пользователя")
    await Ban.ban_id.set()
    await call.message.delete()

@dp.message_handler(state=Ban.ban_id)
async def ban_finish(mess: types.Message, state:FSMContext):
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    name = BotDB.cursor.execute("SELECT login FROM users WHERE user_id = ?", (int(mess.text),)).fetchone()
    if len(name) != 1:
        await mess.bot.send_message(mess.from_user.id, "Пользователь не найден")
    else:
        await mess.bot.send_message(mess.from_user.id, f"Пользователь {name[0]} забанен")
        BotDB.cursor.execute("UPDATE users SET status = ? WHERE user_id = ?", ("ban", int(mess.text)))
        BotDB.conn.commit()
    await state.finish()