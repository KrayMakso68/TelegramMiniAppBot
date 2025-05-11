from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from bot.config import config


router = Router()

@router.message(CommandStart())
async def command_start(message: Message):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Запустить приложение 🚀",
                    web_app=WebAppInfo(url=config.WEBAPP_URL),
                )
            ]
        ]
    )
    await message.answer(text="<b>Привет!</b>\n"
                              "Запускай приложение для погружения в интернет!",
                         reply_markup=markup,
                         parse_mode=ParseMode.HTML)
