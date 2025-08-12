from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from loader import dp
from src.depends import audit_repository


@dp.message(F.unsuccessful_payment)
async def process_unsuccessful_payment(message: Message, state: FSMContext):
    # TODO: suggest some solution
    audit_repository.add_row(
        user_telegram_id=message.from_user.id,
        chat_id=message.chat.id,
        fullname=message.chat.full_name,
        username=message.chat.username,
        event_name="paid",
        description=f"User got error",
    )

    await message.reply("Не удалось выполнить платеж!")
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
