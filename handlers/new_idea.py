import config as cfg
from aiogram import types
from main import dp, BotDB
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


class NewIdea(StatesGroup):
    text = State()


@dp.message_handler(lambda message: message.text == "🆕 Предложить идею", state=None)
async def new_idea(mess: types.Message) -> None:
    await mess.bot.delete_message(mess.from_user.id, mess.message_id)
    status = BotDB.cursor.execute("SELECT status FROM users WHERE user_id = ?", (int(mess.from_user.id),)).fetchone()[0]
    if status == 'ban':
        await mess.bot.send_message(mess.from_user.id, "Вы забанены!")
    else:
        ideas = BotDB.cursor.execute("SELECT * FROM `ideas` WHERE `user_id` = ? AND `status` = ?",
                                     (mess.from_user.id, 'wait')).fetchall()
        if len(ideas) == 0:
            await mess.bot.send_message(mess.from_user.id, 'Напишите то, что хотели бы добавить в Нашего бота')
            await NewIdea.text.set()
        else:
            await mess.bot.send_message(mess.from_user.id, "Вашу прошлую идею ещё не рассмотрели!")


@dp.message_handler(state=NewIdea.text)
async def new_idea_text(mess: types.Message, state: FSMContext) -> None:
    buttons = [
        types.InlineKeyboardButton(text="✅ Одобрить", callback_data=f"new_idea_yes_{mess.from_user.id}"),
        types.InlineKeyboardButton(text="❌ Отказать", callback_data=f"new_idea_no_{mess.from_user.id}"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    BotDB.add_idea(mess.from_user.id, mess.from_user.full_name, mess.text)
    await mess.bot.send_message(mess.from_user.id, 'Спасибо за Вашу идею!\nСотрудник скоро рассмотрит Ваше предложение')
    for i in cfg.admin_ids:
        await mess.bot.send_message(i, f'Пользователь {mess.from_user.full_name} предложил новую идею!\n{mess.text}',
                                    reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(lambda call: call.data.startswith('new_idea_yes_'))
async def new_idea_yes(call: types.CallbackQuery) -> None:
    id = call.data[13:]
    status = BotDB.cursor.execute("SELECT * FROM `ideas` WHERE `user_id` = ? AND `status` = ?", (id, 'wait')).fetchall()
    if len(status) == 0:
        await call.bot.send_message(call.from_user.id, "Идея уже рассмотрена")
    else:
        BotDB.cursor.execute("UPDATE `ideas` SET `status` = ? WHERE `user_id` = ? AND `status` = ?", ('yes', id, 'wait'))
        BotDB.conn.commit()
        await call.bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                                 reply_markup=None)
        await call.message.edit_text(f'{call.message.text}\n✅ Одобрено')
        await call.bot.send_message(id, 'Вашу идею одобрили!')


@dp.callback_query_handler(lambda call: call.data.startswith('new_idea_no_'))
async def new_idea_no(call: types.CallbackQuery) -> None:
    id = call.data[12:]
    status = BotDB.cursor.execute("SELECT * FROM `ideas` WHERE `user_id` = ? AND `status` = ?", (id, 'wait')).fetchall()
    if len(status) == 0:
        await call.bot.send_message(call.from_user.id, "Идея уже рассмотрена")
    else:
        BotDB.cursor.execute("UPDATE `ideas` SET `status` = ? WHERE `user_id` = ? AND `status` = ?", ('no', id, 'wait'))
        BotDB.conn.commit()
        await call.bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                                 reply_markup=None)
        await call.message.edit_text(f'{call.message.text}\n❌ Отказано')
        await call.bot.send_message(id, 'Вашу идею отклонили!')
