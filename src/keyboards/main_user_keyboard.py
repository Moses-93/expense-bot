from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class MainUserKeyboard:
    def __init__(self):
        self.main_menu()

    def main_menu(self):
        """Return the main menu keyboard."""
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="➕ Додати витрату"),
                    KeyboardButton(text="📊 Мої витрати"),
                ],
                [
                    KeyboardButton(text="❌ Видалити витрату"),
                    KeyboardButton(text="✏️ Редагувати витрату"),
                ],
            ],
            resize_keyboard=True,
        )
        return keyboard
