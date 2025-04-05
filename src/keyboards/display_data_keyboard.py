from typing import Dict, List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class DisplayData:

    @staticmethod
    def generate_keyboard(
        data: List[Dict],
        text_key: str,
        callback_key: str,
    ) -> InlineKeyboardMarkup:
        keyboard = [
            [
                InlineKeyboardButton(
                    text=i[text_key],
                    callback_data=f"{i[callback_key]}",
                )
            ]
            for i in data
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)