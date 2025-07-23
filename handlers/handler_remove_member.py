import logging

from aiogram.filters import (
    ChatMemberUpdatedFilter,
    IS_NOT_MEMBER,
    IS_MEMBER,
)
from aiogram.types import ChatMemberUpdated

from loader import dp

logging.basicConfig(level=logging.INFO)


@dp.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def handler_remove_member(event: ChatMemberUpdated):
    logging.info(
        f"Пользователь {event.new_chat_member.user.full_name}, {event.new_chat_member.user.id}"
        f" покинул чат {event.chat.id}"
    )
