import logging
from typing import Dict, Optional
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.keyboards.display_data_keyboard import DisplayData
from src.services.api_client import APIClient

from src.states.expenses import UpdateExpenseStates
from src.services.expense import (
    expense_service as exp_service,
)
from src.handlers.expense import base_handler, messages
from src.utils.expense_validators import (
    amount_validator,
    date_validator,
    name_validator,
)


logger = logging.getLogger(__name__)

STATES = {
    "id": UpdateExpenseStates.EXPENSE_ID,
    "title": UpdateExpenseStates.NAME,
    "date": UpdateExpenseStates.DATE,
    "amount": UpdateExpenseStates.AMOUNT,
}


class ExpenseUpdateHandler(base_handler.BaseExpenseHandler):
    def __init__(self, api_client: APIClient):
        super().__init__(
            messages.UPDATE_EXPENSE_MESSAGES,
            {
                "title": name_validator,
                "date": date_validator,
                "amount": amount_validator,
            },
            {
                "title": "invalid_title",
                "date": "invalid_date",
                "amount": "invalid_uah_amount",
            },
        )
        self.api_client = api_client

    async def handle_start_update_expense(self, message: Message, state: FSMContext):
        await state.clear()
        expense_data = await exp_service.JSONExpenseReportService().execute(
            message.from_user.id, self.api_client
        )
        expense_keyboard = DisplayData.generate_keyboard(
            expense_data, ("title", "date", "uah_amount"), ("id",)
        )
        await state.set_state(STATES["id"])
        await message.answer(self.messages.get("start"), reply_markup=expense_keyboard)

    async def set_expense_id(self, callback: CallbackQuery, state: FSMContext):
        await state.update_data(id=callback.data)
        await state.set_state(STATES["title"])
        await self._send_next(callback.message, "title")

    async def handle_set_name(self, message: Message, state: FSMContext):
        await self._handle(message, state, "title", "date", STATES["date"])

    async def handle_set_date(self, message: Message, state: FSMContext):
        await self._handle(message, state, "date", "amount", STATES["amount"])

    async def handle_set_amount(self, message: Message, state: FSMContext):
        await self._handle(message, state, "amount")

    async def handle_skip(self, callback: CallbackQuery, state: FSMContext):

        current_field = callback.data.split("_")[1]
        fields = list(STATES.keys())
        next_field = (
            fields[fields.index(current_field) + 1]
            if current_field in fields[:-1]
            else None
        )
        if next_field:
            await self._send_next(callback.message, next_field)
        else:
            await self._finalize_update(callback.message, state)

    async def _handle(
        self,
        message: Message,
        state: FSMContext,
        field: str,
        next_field: Optional[str] = None,
        next_state: Optional[str] = None,
    ):
        success = await super()._handle(message, state, field, next_state)
        if not success:
            return

        if next_field:
            await self._send_next(message, next_field)
        else:
            await self._finalize_update(message, state)

    async def _send_next(self, message: Message, next_field: str):
        text, skip_callback = self.messages.get_step_message(next_field)
        keyboard = self.__build_skip_keyboard(skip_callback)

        await message.answer(text, reply_markup=keyboard)

    def __build_skip_keyboard(self, skip_callback: str):
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="⏭️ Пропустити", callback_data=skip_callback)
        return keyboard.as_markup()

    async def _finalize_update(self, message: Message, state: FSMContext):
        data = await state.get_data()
        expense_id = data.pop("id")

        if data:
            service = exp_service.ExpenseMutationService(
                self.api_client, message.from_user.id
            )
            updated_expense: Dict = await service.update(expense_id, data)

            await message.answer(
                self.messages.get("success_update").format(
                    title=updated_expense.get("title", " - "),
                    date=updated_expense.get("date", " - "),
                    amount=updated_expense.get("uah_amount", " - "),
                )
            )
        else:
            await message.answer(self.messages.get("no_changes"))

        await state.clear()
