import logging

from aiogram.filters import (
    ChatMemberUpdatedFilter,
    IS_NOT_MEMBER,
    IS_MEMBER,
)
from aiogram.types import (
    ChatMemberUpdated
)

from src.database import get_active_user
from loader import dp, bot


@dp.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def handle_add_member(event: ChatMemberUpdated):
    logging.info(
        f"Пользователь {event.new_chat_member.user.full_name}, {event.new_chat_member.user.id}"
        f" добавлен в чат {event.chat.id}"
    )

    if get_active_user(
            customer_telegram_id=event.new_chat_member.user.id
    ) is None:
        logging.info(
            f"Пользователь {event.new_chat_member.user.full_name}, {event.new_chat_member.user.id}"
            f" не имеет активной подписки"
        )

        bot.ban_chat_member(
            chat_id=event.chat.id,
            user_id=event.new_chat_member.user.id
        )
        bot.unban_chat_member(
            chat_id=event.chat.id,
            user_id=event.new_chat_member.user.id
        )
    else:
        logging.info(
            f"Пользователь {event.new_chat_member.user.full_name}, {event.new_chat_member.user.id}"
            f" имеет активную подписку"
        )
