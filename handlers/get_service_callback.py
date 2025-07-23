import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.methods.create_invoice_link import LabeledPrice

from config import PROVIDER_TOKEN
from src.database import (
    add_row,
    Deals,
)
from loader import (
    dp,
    bot,
)


@dp.callback_query(lambda c: c.data.startswith("subcription_"))
async def callback_1m(callback: CallbackQuery, state: FSMContext):
    month_count = callback.data.replace('subcription_', '')

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

        add_row(
            table=Deals,
            customer_telegram_id=callback.from_user.id,
            service_months=month_count
        )
    except Exception as e:
        logging.error(f"Ошибка при SendInvoice: {e}")
