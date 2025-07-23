import logging

import asyncio

from loader import bot

logging.basicConfig(level=logging.INFO)


async def main():
    from handlers import dp

    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
