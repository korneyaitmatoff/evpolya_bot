import logging

import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    PreCheckoutQuery,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.methods.create_invoice_link import LabeledPrice

from config import TOKEN

dp = Dispatcher()
bot = Bot(token=TOKEN)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(text=f"Привет, {message.from_user.full_name}!")

    # check subscription
    await message.answer(text="Проверяем подписку...")

    builder = InlineKeyboardBuilder()
    builder.attach(InlineKeyboardBuilder.from_markup(InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1 месяц", callback_data="subcription_1"),
                InlineKeyboardButton(text="3 месяца", callback_data="subcription_3")
            ],
        ]
    )))

    await message.answer(
        text="У вас нет активной подписки. Для приобритения подписки выберите нужную подписку",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(lambda c: c.data.startswith("subcription_"))
async def callback_1m(callback: CallbackQuery):
    month_count = callback.data.replace('subcription_', '')

    await callback.message.answer(text=f"Вы выбрали {month_count} месяц(а)")

    try:
        await bot.send_invoice(
            chat_id=callback.from_user.id,
            title=f"Подписка на {month_count} месяц(а)",
            description="К оплате:",
            payload="Счет на оплату",
            currency="RUB",
            prices=[
                LabeledPrice(
                    label=f"Подписка на {month_count} месяц(а)",
                    amount=100 * (int(month_count) * 100)
                )
            ],
            provider_token="381764678:TEST:127140",
        )
    except Exception as e:
        logging.error(f"Ошибка при SendInvoice: {e}")


@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)  # всегда отвечаем утвердительно
    except Exception as e:
        logging.error(f"Ошибка при обработке апдейта типа PreCheckoutQuery: {e}")


@dp.message(F.successful_payment)
async def process_successful_payment(message: Message, state: FSMContext):
    await message.reply(f"Платеж на сумму {message.successful_payment.total_amount // 100} "
                        f"{message.successful_payment.currency} прошел успешно!")
    logging.info(f"Получен платеж от {message.from_user.id}")
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()


@dp.message(F.unsuccessful_payment)
async def process_unsuccessful_payment(message: Message, state: FSMContext):
    await message.reply("Не удалось выполнить платеж!")
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
