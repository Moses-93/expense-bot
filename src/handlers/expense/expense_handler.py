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


class ExpenseCreateHandler(BaseExpenseHandler):
    def __init__(self, api_client: APIClient):
        super().__init__(api_client, messages.ADD_EXPENSE_MESSAGES)

    async def handle_add_expense(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(expenses.AddExpenseStates.ADD_EXPENSE_NAME)
        await message.answer(self.messages.get("start"), parse_mode="Markdown")

    async def handle_set_expense_name(self, message: Message, state: FSMContext):
        success = await self._handle_field_input(
            message,
            state,
            field="name",
        )
        if success:
            await state.set_state(expenses.AddExpenseStates.ADD_EXPENSE_DATE),

        await message.answer(self.messages.get("set_date"), parse_mode="Markdown")

    async def handle_set_expense_date(self, message: Message, state: FSMContext):
        success = await self._handle_field_input(
            message,
            state,
            field="date",
        )
        if success:
            await state.set_state(expenses.AddExpenseStates.ADD_EXPENSE_AMOUNT),
        await message.answer(self.messages.get("set_amount"), parse_mode="Markdown")

    async def handle_set_expense_amount(self, message: Message, state: FSMContext):
        await self._handle_field_input(message, state, field="uah_amount")

        await self._finalize_creation(message, state)

    async def _finalize_creation(self, message: Message, state: FSMContext):
        data = await state.get_data()
        logger.debug(f"{data=}")
        service = exp_service.ExpenseMutationService(
            self.api_client, message.from_user.id
        )
        created_expense = await service.create(data)
        await message.answer(
            self.messages.get("success_create").format(
                name=created_expense.get("name", "-"),
                date=created_expense.get("date", "-"),
                amount=created_expense.get("uah_amount", "-"),
            )
        )
        await state.clear()


class ExpenseGetReportHandler(BaseExpenseHandler):
    def __init__(self, api_client: APIClient):
        super().__init__(api_client, messages.GET_EXPENSE_MESSAGES)

    def _get_validator(self, field: str):
        if field in ("start_date", "end_date"):
            return date_validator
        return super()._get_validator(field)

    async def handle_start(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(expenses.GetExpensesReportStates.START_DATE)
        await message.answer(self.messages.get("start"), parse_mode="Markdown")

    async def handle_set_start_date(self, message: Message, state: FSMContext):
        is_valid = await self._handle_field_input(message, state, "start_date")
        if is_valid:
            await state.set_state(expenses.GetExpensesReportStates.END_DATE)
            await message.answer(
                self.messages.get("set_end_date"), parse_mode="Markdown"
            )

    async def handle_set_end_date(self, message: Message, state: FSMContext):
        is_valid = await self._handle_field_input(message, state, "end_date")
        if is_valid:
            await self.handle_generate_expense_report(message, state)

    async def handle_generate_expense_report(self, message: Message, state: FSMContext):
        data = await state.get_data()
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        await state.clear()

        try:
            service = exp_service.FileExpenseReportService("xlsx", start_date, end_date)
            report_file = await service.execute(
                user_id=message.from_user.id, api_client=self.api_client
            )
            await message.answer_document(report_file)
        except ValueError as e:
            await message.answer(str(e))


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
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.messages = MessageManager(messages.DELETE_EXPENSE_MESSAGES)

    async def start(self, message: Message, state: FSMContext):
        await state.clear()
        expense_data = await exp_service.JSONExpenseReportService().execute(
            message.from_user.id, self.api_client
        )
        expense_keyboard = DisplayData.generate_keyboard(
            expense_data, ("name", "date", "uah_amount"), ("id",)
        )
        await state.set_state(expenses.DeleteExpenseStates.EXPENSE_ID)
        await message.answer(self.messages.get("start"), reply_markup=expense_keyboard)

    async def handle_delete_expense(self, callback: CallbackQuery, state: FSMContext):

        service = exp_service.ExpenseMutationService(
            self.api_client, callback.from_user.id
        )
        await service.delete(callback.data)

        await callback.message.answer(
            self.messages.get("success_delete"), parse_mode="Markdown"
        )
        await state.clear()
