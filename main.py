import config as cfg
import aiogram as a
import aiogram.utils.markdown as fmt
from aiogram.utils.emoji import emojize
import logging
from db import BotDB
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = a.Bot(token=cfg.TOKEN, parse_mode="HTML")
BotDB = BotDB('db.db')
dp = a.Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)