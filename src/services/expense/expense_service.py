import logging
from aiogram.types import BufferedInputFile

from .expense_api_client import ExpenseAPIClient

logger = logging.getLogger(__name__)


class ExpenseReportService:

    def __init__(self, expense_api_client: ExpenseAPIClient):
        self.expense_api_client = expense_api_client

    async def format_report_from_bytes(
        self, byte_report: bytes, filename: str
    ) -> BufferedInputFile:
        return BufferedInputFile(byte_report, filename)

    async def get_expenses_report(
        self, user_id: int, start_date: str, end_date: str, report_type: str = "excel"
    ):
        byte_report = await self.expense_api_client.get_expenses_report(
            user_id, start_date, end_date, report_type
        )
        return await self.format_report_from_bytes(
            byte_report, f"ExpenseReport_{start_date}_{end_date}"
        )
