from typing import Dict, List, Tuple
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class DisplayData:

    @staticmethod
    def generate_keyboard(
        data: List[Dict],
        text_keys: Tuple[str],
        callback_key: Tuple[str],
    ) -> InlineKeyboardMarkup:
        keyboard = [
            [
                InlineKeyboardButton(
                    text=" - ".join(str(i.get(key, "...")) for key in text_keys),
                    callback_data=f"{" ".join(str(i.get(key, "...")) for key in callback_key)}",
                )
            ]
            for i in data
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
