import asyncio
import logging
from aiogram import Dispatcher, Bot

from app.middleware.anti_spam_middleware import AntiSpamMiddleware
from app.handlers.handler_start import router_start
from app.handlers.handler_chat_member import router_chat_member
from app.handlers.handler_rating import router_rating
from app.handlers.handler_my_photos import router_my_photos
from app.handlers.handler_groups import router_groups
from app.handlers.service_handlers import router_service_handlers
from app.handlers.handler_download_a_photos import router_download_photos
from app.handlers.handler_archive import router_archive
from app.middleware.logging_middleware import UserActionLoggingMiddleware

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def setup_logging_middlewares(dp: Dispatcher):
    logging_middleware = UserActionLoggingMiddleware()

    for name, observer in dp.observers.items():
        # update можно пропустить, чтобы не было дублей
        # error тоже можно пропустить, если не нужно
        if name in {"update", "error"}:
            continue

        observer.middleware(logging_middleware)

async def main():
    spam_middleware = AntiSpamMiddleware()

    setup_logging_middlewares(dp)
    dp.update.outer_middleware(spam_middleware)

    dp.include_routers(router_start, router_chat_member, router_rating, router_my_photos, router_groups, router_service_handlers, router_download_photos, router_archive)
    await dp.start_polling(bot)

if __name__ == '__main__':
    file_log = logging.FileHandler('logging.log')
    console_out = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO, handlers=(file_log, console_out))
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
        logging.info("Программа завершила работу по Ctrl + C")
    except Exception as e:
        logging.info(f'{e}')