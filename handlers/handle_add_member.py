import logging

from aiogram.filters import (
    ChatMemberUpdatedFilter,
    IS_NOT_MEMBER,
    IS_MEMBER,
)
from aiogram.types import (
    ChatMemberUpdated
)

from loader import dp, bot
from src.depends import (
    customer_repository,
    audit_repository
)


@dp.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def handle_add_member(event: ChatMemberUpdated):
    logging.info(
        f"Пользователь {event.new_chat_member.user.full_name}, {event.new_chat_member.user.id}"
        f" добавлен в чат {event.chat.id}"
    )

    audit_repository.add_row(
        user_telegram_id=event.from_user.id,
        chat_id=event.chat.id,
        fullname=event.from_user.full_name,
        username=event.from_user.username,
        event_name="add_to_group",
        description=f"User added to group",
    )

    if customer_repository.get_active_user(
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
