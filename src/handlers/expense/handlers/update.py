import logging
from typing import Dict
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.keyboards.display_data_keyboard import DisplayData
from src.services.api_client import APIClient

from src.states import expenses
from src.services.expense import (
    expense_service as exp_service,
    step_resolver as exp_fsm,
)
from src.handlers.expense import base_handler, messages


logger = logging.getLogger(__name__)


class ExpenseUpdateHandler(base_handler.BaseExpenseHandler):
    def __init__(self, api_client: APIClient):
        super().__init__(api_client, messages.UPDATE_EXPENSE_MESSAGES)

    async def handle_start_update_expense(self, message: Message, state: FSMContext):
        await state.clear()
        expense_data = await exp_service.JSONExpenseReportService().execute(
            message.from_user.id, self.api_client
        )
        expense_keyboard = DisplayData.generate_keyboard(
            expense_data, ("name", "date", "uah_amount"), ("id",)
        )
        await state.set_state(expenses.UpdateExpenseStates.EXPENSE_ID)
        await message.answer(self.messages.get("start"), reply_markup=expense_keyboard)

    async def set_expense_id(self, callback: CallbackQuery, state: FSMContext):
        await state.update_data(id=callback.data)
        await self._send_next(
            callback.message, state, expenses.UpdateExpenseStates.NAME
        )

    async def handle_set_name(self, message: Message, state: FSMContext):
        await self._handle_field_input(
            message, state, "name", expenses.UpdateExpenseStates.DATE
        )

    async def handle_set_date(self, message: Message, state: FSMContext):
        await self._handle_field_input(
            message, state, "date", expenses.UpdateExpenseStates.AMOUNT
        )

    async def handle_set_amount(self, message: Message, state: FSMContext):
        await self._handle_field_input(message, state, "uah_amount")

    async def handle_skip(self, callback: CallbackQuery, state: FSMContext):
        current_state = await state.get_state()
        next_state = exp_fsm.next_step(current_state)

        if next_state:
            await self._send_next(callback.message, state, next_state)
        else:
            await self._finalize_update(callback.message, state)

    async def _handle_field_input(
        self, message: Message, state: FSMContext, field: str, next_state: str = None
    ):
        success = await super()._handle_field_input(message, state, field)
        if not success:
            return

        if next_state:
            await self._send_next(message, state, next_state)
        else:
            await self._finalize_update(message, state)

    async def _send_next(self, message: Message, state: FSMContext, next_state: str):
        field = exp_fsm.get_field_from_state(next_state)
        text, skip_callback = self.messages.get_step_message(field)

        keyboard = self._build_skip_keyboard(skip_callback)

        await state.set_state(next_state)
        await message.answer(text, reply_markup=keyboard)

    def _build_skip_keyboard(self, skip_callback: str):
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
                    name=updated_expense.get("name", " - "),
                    date=updated_expense.get("date", " - "),
                    amount=updated_expense.get("uah_amount", " - "),
                )
            )
        else:
            await message.answer(self.messages.get("no_changes"))

        await state.clear()
