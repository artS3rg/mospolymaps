from aiogram import types

start_buttons = ["🗺Навигатор", "❓FAQ", "🆕Предложить идею"]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
start_keyboard.add(*start_buttons)

navigation_buttons = ["Большая Семёновская (БС)", "🏠Главная"]
navigation_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
navigation_keyboard.add(*navigation_buttons)

bsCampus_buttons = ["🔻Маршрут", "📖Информация", "🏠Главная"]
bsCampus_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
bsCampus_keyboard.add(*bsCampus_buttons)
