import logging

from aiogram import Bot, Dispatcher

from config import (
    TOKEN,
)

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
bot = Bot(token=TOKEN)
