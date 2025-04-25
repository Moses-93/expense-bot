import logging
from typing import Dict
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext

from src.states.expenses import GetExpensesReportStates
from src.services.expense.expense_service import ReportGeneratorService
from src.utils.message_provider import MessageProvider
from src.core.messages.enums import GetExpenseMessage
from src.models.expense_dto import ExpenseReportRequestDTO, ExpenseReportFile

logger = logging.getLogger(__name__)


class ExpenseGetReportHandler:
    def __init__(
        self,
        report_generator: ReportGeneratorService,
        message_provider: MessageProvider[GetExpenseMessage],
    ):
        self.report_generator = report_generator
        self._messages = message_provider

    async def handle_start(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(GetExpensesReportStates.START_DATE)
        await message.answer(
            self._messages.get(GetExpenseMessage.START_DATE), parse_mode="Markdown"
        )

    async def handle_set_start_date(
        self, message: Message, state: FSMContext, date: str
    ):
        await state.update_data(start_date=date)
        await state.set_state(GetExpensesReportStates.END_DATE)
        await message.answer(
            self._messages.get(GetExpenseMessage.END_DATE), parse_mode="Markdown"
        )

    async def handle_set_end_date(self, message: Message, state: FSMContext, date: str):
        state_data = await state.update_data(end_date=date)
        await self.handle_generate_expense_report(message, state_data)
        await state.clear()

    async def handle_generate_expense_report(
        self, message: Message, report_request_data: Dict[str, str]
    ):
        request_dto = ExpenseReportRequestDTO(**report_request_data)

        report_file_dto = await self.report_generator.generate_report(
            message.from_user.id, request_dto
        )
        await self._send_report(message, report_file_dto)

    async def _send_report(self, message: Message, report_dto: ExpenseReportFile):
        report_file = BufferedInputFile(
            file=report_dto.content, filename=report_dto.filename
        )
        await message.answer_document(report_file)
