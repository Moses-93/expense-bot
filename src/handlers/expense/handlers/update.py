import logging
from typing import Optional

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.core.messages.enums import UpdateExpenseMessage, ErrorMessage
from src.core.messages.texts.error_message import ERROR_MESSAGES
from src.states.expenses import UpdateExpenseStates
from src.services.expense import expense_service
from src.utils.message_provider import MessageProvider
from src.models.expense_dto import UpdateExpenseDTO

logger = logging.getLogger(__name__)

FIELDS_ORDER = ["title", "date", "amount"]

FIELD_STATES = {
    "id": UpdateExpenseStates.EXPENSE_ID,
    "title": UpdateExpenseStates.TITLE,
    "date": UpdateExpenseStates.DATE,
    "amount": UpdateExpenseStates.AMOUNT,
}

FIELD_MESSAGES = {
    "title": UpdateExpenseMessage.SET_TITLE,
    "date": UpdateExpenseMessage.SET_DATE,
    "amount": UpdateExpenseMessage.SET_AMOUNT,
}


class ExpenseUpdateHandler:
    def __init__(
        self,
        mutation_service: expense_service.ExpenseMutationService,
        keyboard_builder: expense_service.ExpenseKeyboardBuilder,
        message_provider: MessageProvider[UpdateExpenseMessage],
    ):
        self.mutation_service = mutation_service
        self.keyboard_builder = keyboard_builder
        self.message_provider = message_provider

    async def handle_start(self, message: Message, state: FSMContext):
        await state.clear()

        expenses_keyboard = await self.keyboard_builder.build_keyboard(
            message.from_user.id
        )
        await state.set_state(UpdateExpenseStates.EXPENSE_ID)

        await message.answer(
            self.message_provider.get(UpdateExpenseMessage.START),
            reply_markup=expenses_keyboard,
        )

    async def set_expense_id(self, callback: CallbackQuery, state: FSMContext):
        await state.update_data(id=callback.data)
        await self._ask_next_field(callback.message, state, "title")

    async def handle_set_title(self, message: Message, state: FSMContext, title: str):
        await self._save_and_next(message, state, "title", title)

    async def handle_set_date(self, message: Message, state: FSMContext, date: str):
        await self._save_and_next(message, state, "date", date)

    async def handle_set_amount(
        self, message: Message, state: FSMContext, amount: float
    ):
        await self._save_and_next(message, state, "amount", amount)

    async def handle_skip(self, callback: CallbackQuery, state: FSMContext):
        current_field = callback.data.split("_", maxsplit=1)[1]
        next_field = self._get_next_field(current_field)

        if next_field:
            await self._ask_next_field(callback.message, state, next_field)
        else:
            await self._finalize_update(callback.message, state)

    async def _save_and_next(
        self, message: Message, state: FSMContext, field: str, value
    ):
        await state.update_data(**{field: value})

        next_field = self._get_next_field(field)
        if next_field:
            await self._ask_next_field(message, state, next_field)
        else:
            await self._finalize_update(message, state)

    async def _ask_next_field(self, message: Message, state: FSMContext, field: str):
        await state.set_state(FIELD_STATES[field])

        text = self.message_provider.get(FIELD_MESSAGES[field])
        keyboard = self.__build_skip_keyboard(f"skip_{field}")

        await message.answer(text, reply_markup=keyboard)

    async def _finalize_update(self, message: Message, state: FSMContext):
        state_data = await state.get_data()
        expense_id = state_data.pop("id", None)

        if state_data:
            try:
                expense_data = UpdateExpenseDTO(**state_data)
            except ValueError:
                await message.answer(ERROR_MESSAGES[ErrorMessage.INVALID_DATA])
                return
            await self.mutation_service.update(
                expense_id, message.from_user.id, expense_data
            )

            await message.answer(
                self.message_provider.get(UpdateExpenseMessage.SUCCESS).format(
                    title=expense_data.title,
                    date=expense_data.date,
                    amount=expense_data.amount,
                )
            )
        else:
            await message.answer(ERROR_MESSAGES[ErrorMessage.NO_CHANGES])

        await state.clear()

    def __build_skip_keyboard(self, skip_callback: str):
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="⏭️ Пропустити", callback_data=skip_callback)
        return keyboard.as_markup()

    def _get_next_field(self, current_field: str) -> Optional[str]:
        try:
            idx = FIELDS_ORDER.index(current_field)
            return FIELDS_ORDER[idx + 1] if idx + 1 < len(FIELDS_ORDER) else None
        except ValueError:
            return None
