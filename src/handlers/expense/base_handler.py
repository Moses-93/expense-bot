from typing import Callable, Dict, Optional, Tuple, Union
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from src.utils.message_manager import MessageManager


class BaseExpenseHandler:

    def __init__(
        self,
        messages: Dict[str, str],
        validators: Dict[str, Callable],
        error_keys: Dict[str, str],
    ):
        self._validators = validators
        self._error_keys = error_keys
        self.messages = MessageManager(messages)

    async def _handle(
        self,
        message: Message,
        state: FSMContext,
        field: Optional[str] = None,
        next_state: Optional[State] = None,
    ) -> bool:

        value = message.text
        if value and field:
            ok, error_key, value = self._validate(field, value)

            if not ok:
                await message.answer(self.messages.get(error_key))
                return False

            await state.update_data({field: value})
        if next_state:
            await state.set_state(next_state)
        return True

    def _validate(
        self, field: str, raw_value: str
    ) -> Tuple[bool, Union[str, None], any]:

        validator = self._validators.get(field)
        if not validator:
            raise ValueError(f"Unknown field: {field}")

        result = validator(raw_value)
        if result is None:
            return False, self._error_keys[field], None
        return True, None, result
