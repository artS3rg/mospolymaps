from aiogram import types
from main import BotDB

start_buttons = ["🗺 Навигатор", "🆕 Предложить идею", "💬 Помощник"]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
start_keyboard.add(*start_buttons)

navigation_buttons = ["Большая Семёновская (БС)", "🏠 Главная"]
navigation_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
navigation_keyboard.add(*navigation_buttons)

bsCampus_buttons = ["🔻 Маршрут (БС)", "📖 Информация (БС)", "🏠 Главная"]
bsCampus_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
bsCampus_keyboard.add(*bsCampus_buttons)

helper_main_sections_buttons = ["📖 Разделы", "🔎 Поиск", "🏠 Главная"]
helper_main_sections_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
helper_main_sections_keyboard.add(*helper_main_sections_buttons)

informational_sections_buttons = BotDB.get_sections() + ["↩ Назад"]
informational_sections_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
informational_sections_keyboard.add(*informational_sections_buttons)
