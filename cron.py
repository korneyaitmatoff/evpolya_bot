import asyncio
from datetime import datetime

from sqlalchemy.orm import Session

from src.depends import customer_repository

from app import bot


async def main():
    for customer in customer_repository.get_expired_customers():
        await bot.ban_chat_member(
            chat_id=customer.chat_id,
            user_id=customer.telegram_id
        )


if __name__ == "__main__":
    asyncio.run(main())
