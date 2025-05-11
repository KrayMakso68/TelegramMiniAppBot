import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import WebAppInfo, MenuButtonWebApp

from bot.services.scheduler import Scheduler
from config import config


async def on_startup(bot: Bot):
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Запустить 🚀", web_app=WebAppInfo(url=config.WEBAPP_URL))
    )


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    bot = Bot(token=config.TOKEN)
    dp = Dispatcher()

    from bot.handlers import commands
    dp.include_router(commands.router)

    try:
        dp.startup.register(on_startup)
        scheduler = Scheduler(bot)
        asyncio.create_task(scheduler.start())

        await dp.start_polling(bot)
    finally:
        await scheduler.stop()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
        print('Run')
    except KeyboardInterrupt:
        print('Exit')
