from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.services.api_client import APIClient
from src.utils.message_manager import MessageManager
from src.utils.expense_validators import (
    date_validator,
    amount_validator,
    name_validator,
)


class BaseExpenseHandler:
    VALIDATORS = {
        "name": name_validator,
        "date": date_validator,
        "uah_amount": amount_validator,
    }

    def __init__(self, api_client: APIClient, messages: dict):
        self.api_client = api_client
        self.messages = MessageManager(messages)

    def _get_validator(self, field: str):
        return self.VALIDATORS.get(field)

    async def _handle_field_input(
        self,
        message: Message,
        state: FSMContext,
        field: str,
    ) -> bool:
        value = message.text

        if value:
            valid_value = self._get_validator(field)(value)

            if not valid_value:
                await message.answer(self.messages.get(f"invalid_{field}"))
                return False

            await state.update_data({field: valid_value})

        return True
