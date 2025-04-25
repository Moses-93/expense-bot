import logging
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from src.core.messages.enums import ErrorMessage
from src.utils.message_manager import MessageProvider

logger = logging.getLogger(__name__)

class ValidationErrorHandler:
    _ERROR_MAPPING = {
        "AMOUNT": ErrorMessage.INVALID_AMOUNT,
        "DATE": ErrorMessage.INVALID_DATE,
        "TITLE": ErrorMessage.INVALID_TITLE,
    }

    def __init__(self, message_provider: MessageProvider[ErrorMessage]):
        self._message_provider = message_provider

    async def handle_error(self, message: Message, state: FSMContext):
        current_state = await state.get_state()
        error_key = next(
            (key for key in self._ERROR_MAPPING if key.lower() in current_state.lower()),
            None
        )
        
        if error_key:
            error_msg = self._message_provider.get(self._ERROR_MAPPING[error_key])
            await message.answer(error_msg, parse_mode="Markdown")
        else:
            logger.warning(f"State {current_state} not found in error mapping.")
            await message.answer("❌ Ой, сталося щось не зрозуміле. Спробуйте пізніше")