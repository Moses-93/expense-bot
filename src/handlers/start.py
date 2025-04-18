from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.keyboards.user_keyboard import MainUserKeyboard

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    """Handle the /start command and the start button in the main menu."""
    await message.answer(
        "Привіт! Я бот для управління витратами." "Виберіть дію з меню нижче.",
        reply_markup=MainUserKeyboard().main_menu(),
    )
