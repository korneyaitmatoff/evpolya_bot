import logging

from aiogram.types import PreCheckoutQuery
from loader import (
    dp,
    bot,
)


@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    except Exception as e:
        logging.error(f"Ошибка при обработке апдейта типа PreCheckoutQuery: {e}")
