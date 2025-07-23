import logging

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import GROUP_ID
from src.database import (
    add_row,
    Customers,
    set_success_deals,
    set_expired_date,
    get_deal_by_customer_telegram_id,
)
from loader import bot, dp

logging.basicConfig(level=logging.INFO)


@dp.message(F.successful_payment)
async def process_successful_payment(message: Message, state: FSMContext):
    await message.reply(
        f"Платеж на сумму {message.successful_payment.total_amount // 100} "
        f"{message.successful_payment.currency} прошел успешно!"
    )
    logging.info(f"Получен платеж от {message.from_user.id}")
    current_state = await state.get_state()

    if current_state is not None:
        await state.clear()

    add_row(
        table=Customers,
        name=message.from_user.full_name,
        telegram_id=message.from_user.id,
        chat_id=GROUP_ID
    )
    set_success_deals(
        customer_id=message.from_user.id
    )
    set_expired_date(
        customer_telegram_id=message.from_user.id,
        months=get_deal_by_customer_telegram_id(customer_telegram_id=message.from_user.id).service_months
    )

    # ???
    invite_link = await bot.create_chat_invite_link(
        chat_id=GROUP_ID,
        member_limit=1
    )

    await message.reply(f"Ссылка на подписку: {invite_link.invite_link}")
