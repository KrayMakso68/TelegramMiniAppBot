import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, MenuButtonWebApp

from config import TOKEN, WEBAPP_URL

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def on_startup(bot: Bot):
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Запустить 🚀", web_app=WebAppInfo(url=WEBAPP_URL))
    )


@dp.message(CommandStart())
async def command_start(message: Message):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Запустить приложение 🚀",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ]
        ]
    )
    await message.answer(text="<b>Привет!</b>\n"
                              "Запускай приложение для погружения в интернет!",
                         reply_markup=markup,
                         parse_mode=ParseMode.HTML)


async def main():
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == '__main__':
    print('Run')
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
