import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramAPIError
from aiogram.types import BotCommand
from middleware.admin_only import AdminOnlyMiddlware
from middleware.rate_limit import RateLimitMiddleware
from dotenv import load_dotenv
import os

from handlers import routes

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=MemoryStorage())

    # dp.message.middleware(AdminOnlyMiddlware())
    dp.message.middleware(RateLimitMiddleware(limit_seconds=1.0))

    dp.include_router(routes.router)

    await bot.set_my_commands([
        BotCommand(command='start', description='Start working'),
        BotCommand(command='add', description='Add user'),
        BotCommand(command='users', description='List all users'),
        BotCommand(command='get', description='Get user by ID'),
        BotCommand(command='update', description='Update user by ID'),
        BotCommand(command='delete', description='Delete user by ID'),
    ])

    # await routes.init_db()

    try:
        await dp.start_polling(bot)
    except TelegramAPIError as e:
        logging.error(f'Error starting TelegramAPIError: {e}')
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())