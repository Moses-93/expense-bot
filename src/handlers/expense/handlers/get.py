import logging
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.services.api_client import APIClient

from src.states.expenses import GetExpensesReportStates
from src.utils.expense_validators import date_validator
from src.services.expense import expense_service as exp_service

from src.handlers.expense.base_handler import BaseExpenseHandler
from src.handlers.expense.messages import GET_EXPENSE_MESSAGES


logger = logging.getLogger(__name__)


class ExpenseGetReportHandler(BaseExpenseHandler):
    def __init__(self, api_client: APIClient):
        super().__init__(api_client, GET_EXPENSE_MESSAGES)

    def _get_validator(self, field: str):
        if field in ("start_date", "end_date"):
            return date_validator
        return super()._get_validator(field)

    async def handle_start(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(GetExpensesReportStates.START_DATE)
        await message.answer(self.messages.get("start"), parse_mode="Markdown")

    async def handle_set_start_date(self, message: Message, state: FSMContext):
        is_valid = await self._handle_field_input(message, state, "start_date")
        if is_valid:
            await state.set_state(GetExpensesReportStates.END_DATE)
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
