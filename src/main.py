import os
import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.core.config import telegram_api_token
from src.handlers.handler_factory import HandlerFactory
from src.core.middleware.exc_handler import ErrorHandlingMiddleware

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler(),
    ],
)

handler_factory = HandlerFactory()

bot = Bot(token=telegram_api_token)
dp = Dispatcher()
dp.message.middleware(ErrorHandlingMiddleware())
dp.callback_query.middleware(ErrorHandlingMiddleware())


async def main():
    dp.include_router(handler_factory.get_router())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
