import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.methods.create_invoice_link import LabeledPrice

from config import PROVIDER_TOKEN
from src.depends import (
    deals_repository,
    audit_repository
)
from loader import (
    dp,
    bot,
)


@dp.callback_query(lambda c: c.data.startswith("subcription_"))
async def callback_1m(callback: CallbackQuery, state: FSMContext):
    month_count = callback.data.replace('subcription_', '')

    audit_repository.add_row(
        user_telegram_id=callback.message.from_user.id,
        chat_id=callback.message.chat.id,
        fullname=callback.message.chat.full_name,
        username=callback.message.chat.username,
        event_name="choose",
        description=f"User chose {month_count} month",
    )

    await callback.message.answer(text=f"Вы выбрали {month_count} месяц(а)")

    try:
        # TODO: get service's price from database
        current_state = await state.get_state()
        if current_state is not None:
            await state.clear()

        await bot.send_invoice(
            chat_id=callback.from_user.id,
            title=f"Подписка на {month_count} месяц(а)",
            description="К оплате:",
            payload="Счет на оплату",
            currency="RUB",
            prices=[
                LabeledPrice(
                    label=f"Подписка на {month_count} месяц(а)",
                    amount=1999 * 100 if month_count == "1" else 3555 * 100,
                )
            ],
            provider_token=PROVIDER_TOKEN,
        )

        deals_repository.add_row(
            customer_telegram_id=callback.from_user.id,
            service_months=month_count
        )
    except Exception as e:
        logging.error(f"Ошибка при SendInvoice: {e}")
