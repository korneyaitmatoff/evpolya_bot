import asyncio
from datetime import datetime

from sqlalchemy.orm import Session

from src.database import (
    engine,
    Customers
)

from app import bot


async def main():
    with Session(bind=engine) as session:
        data = session.query(Customers).filter(
            Customers.expired_at < datetime.now()
        ).all()

        for customer in data:
            await bot.ban_chat_member(
                chat_id=customer.chat_id,
                user_id=customer.telegram_id
            )


if __name__ == "__main__":
    asyncio.run(main())
