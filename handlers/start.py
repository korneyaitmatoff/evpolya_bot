from pyexpat.errors import messages

from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import dp
from src.depends import (
    customer_repository,
    audit_repository
)


@dp.message(CommandStart())
async def start_message(message: Message):
    audit_repository.add_row(
        user_telegram_id=message.from_user.id,
        chat_id=message.chat.id,
        fullname=message.from_user.full_name,
        username=message.from_user.username,
        event_name="start",
        description="User pressed start",
    )

    await message.answer(text=f"Привет, {message.from_user.full_name}!")

    await message.answer(text="Проверяем подписку...")

    # TODO: get services from database
    builder = InlineKeyboardBuilder()
    builder.attach(InlineKeyboardBuilder.from_markup(InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1 месяц", callback_data="subcription_1"),
                InlineKeyboardButton(text="3 месяца", callback_data="subcription_3")
            ],
        ]
    )))

    if customer_repository.get_active_user(
            customer_telegram_id=message.from_user.id
    ) is None:
        await message.answer(
            text="У вас нет активной подписки. Для приобретения подписки выберите нужную подписку",
            reply_markup=builder.as_markup()
        )
    else:
        await message.answer(
            text="У вас уже есть активная подписка"
        )

        await message.answer(
            text="Однако вы можете ее продлить! Для этого выберите нужную подписку",
            reply_markup=builder.as_markup()
        )
