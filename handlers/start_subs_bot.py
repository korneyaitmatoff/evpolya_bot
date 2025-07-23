from loader import bot, dp

from aiogram.filters import Command


@dp.message(Command("start_subs_bot"))
async def start_subs_bot(message):
    print(message.chat.id)

    # TODO: save to db
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
