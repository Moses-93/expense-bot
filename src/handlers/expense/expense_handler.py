import logging
from typing import Dict
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.keyboards.display_data_keyboard import DisplayData
from src.services.api_client import APIClient

from src.states import expenses
from src.utils.message_manager import MessageManager
from src.utils.expense_validators import date_validator
from src.services.expense import (
    expense_service as exp_service,
    step_resolver as exp_fsm,
)
from .base_handler import BaseExpenseHandler
from . import messages


logger = logging.getLogger(__name__)


class ExpenseCreateHandler:

    def __init__(self, fsm_service: add_expense_fsm.AddExpenseFSMService):
        self.fsm_service = fsm_service

    async def handle_add_expense(self, message: Message, state: FSMContext):
        msg = await self.fsm_service.start(state)
        await message.answer(msg, parse_mode="Markdown")

    async def handle_set_expense_name(self, message: Message, state: FSMContext):
        msg = await self.fsm_service.set_name(state, message.text)
        await message.answer(msg, parse_mode="Markdown")

    async def handle_set_expense_date(self, message: Message, state: FSMContext):
        """Handle the 'Додати витрату' button."""
        msg = await self.fsm_service.set_date(state, message.text)
        await message.answer(msg, parse_mode="Markdown")

    async def handle_set_expense_amount(self, message: Message, state: FSMContext):
        """Handle the 'Додати витрату' button."""
        msg = await self.fsm_service.set_amount(
            state, message.from_user.id, message.text
        )
        await message.answer(msg, parse_mode="Markdown")


class ExpenseGetReportHandler:

    def __init__(self, fsm_service: get_expense_report_fsm.GetReportFSMService):
        self.fsm_service = fsm_service

    async def handle_start_expense_report(self, message: Message, state: FSMContext):
        msg = await self.fsm_service.start(state)
        await message.answer(msg, parse_mode="Markdown")

    async def handle_set_report_start_date(self, message: Message, state: FSMContext):
        msg = await self.fsm_service.set_start_date(message.text, state)
        await message.answer(msg, parse_mode="Markdown")

    async def handle_generate_expense_report(self, message: Message, state: FSMContext):
        msg, report = await self.fsm_service.set_end_date(
            message.from_user.id, message.text, state
        )
        if report:
            return await message.answer_document(report, caption=msg)
        await message.answer(msg)


class ExpenseUpdateHandler:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.messages = MessageManager(messages.UPDATE_EXPENSE_MESSAGES)

    async def handle_start_update_expense(self, message: Message, state: FSMContext):
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
        value = message.text
        if value:
            valid_value = VALIDATORS[field](value)
            if not valid_value:
                return await message.answer(self.messages.get(f"invalid_{field}"))
            await state.update_data({field: valid_value})
        if next_state:
            await self._send_next(message, state, next_state)
        else:
            await self._finalize_update(message, state)

    async def _send_next(self, message: Message, state: FSMContext, next_state: str):
        field = exp_fsm.get_field_from_state(next_state)
        text, skip_callback = self.messages.get_step_message(field)

        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="⏭️ Пропустити", callback_data=skip_callback)

        await state.set_state(next_state)
        await message.answer(text, reply_markup=keyboard.as_markup())

    async def _finalize_update(self, message: Message, state: FSMContext):
        data = await state.get_data()
        expense_id = data.pop("id")

        if data:
            service = exp_service.ExpenseUpdateService(
                self.api_client, message.from_user.id
            )
            updated_expense: Dict = await service.update_expense(data, expense_id)

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


class ExpenseDeleteHandler:

    def __init__(self, fsm_service: delete_expense_fsm.DeleteFSMService):
        self.fsm_service = fsm_service

    async def start(self, message: Message, state: FSMContext):
        msg, report = await self.fsm_service.start_delete_expense(
            message.from_user.id, state
        )
        if report:
            return await message.answer_document(report, caption=msg)
        await message.answer(msg)

    async def handle_delete_expense(self, message: Message, state: FSMContext):
        msg = await self.fsm_service.delete_expense(
            message.from_user.id, message.text, state
        )
        await message.answer(msg, parse_mode="Markdown")
