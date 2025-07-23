from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from loader import dp


@dp.message(F.unsuccessful_payment)
async def process_unsuccessful_payment(message: Message, state: FSMContext):
    # TODO: suggest some resolution
    await message.reply("Не удалось выполнить платеж!")
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
