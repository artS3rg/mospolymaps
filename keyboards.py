from aiogram import types
from main import BotDB

start_stud_buttons = ["🗺 Навигатор", "🆕 Предложить идею", "💬 Помощник"]
start_stud_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
start_stud_keyboard.add(*start_stud_buttons)

start_staff_buttons = BotDB.get_employee_sections() + ["↩ Назад"]
start_staff_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
start_staff_keyboard.add(*start_staff_buttons)

navigation_buttons = ["Большая Семёновская (БС)", "🏠 Главная"]
navigation_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
navigation_keyboard.add(*navigation_buttons)

bsCampus_buttons = ["🔻 Маршрут (БС)", "📖 Информация (БС)", "🏠 Главная"]
bsCampus_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
bsCampus_keyboard.add(*bsCampus_buttons)

helper_main_sections_buttons = ["📖 Разделы", "🔎 Поиск", "🏠 Главная", "📚 Расписание"]
helper_main_sections_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
helper_main_sections_keyboard.add(*helper_main_sections_buttons)

informational_sections_buttons = BotDB.get_sections() + ["↩ Назад"]
informational_sections_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
informational_sections_keyboard.add(*informational_sections_buttons)

search_back_buttons = ["↩ Выйти из поиска"]
search_back_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
search_back_keyboard.add(*search_back_buttons)

idea_back_buttons = ["↩ Назад"]
idea_back_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
idea_back_keyboard.add(*idea_back_buttons)
