import logging
from typing import Optional
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
        self,
        user_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        all_expenses: Optional[bool] = None,
        report_type: str = "excel",
    ) -> Optional[BufferedInputFile]:
        if all_expenses:
            byte_report = await self.expense_api_client.get_expenses_report(
                user_id, all_expenses=True, report_type=report_type
            )
        else:
            byte_report = await self.expense_api_client.get_expenses_report(
                user_id,
                start_date=start_date,
                end_date=end_date,
                report_type=report_type,
            )

        if not byte_report:
            return None

        filename = self._build_filename(start_date, end_date, report_type)
        return await self.format_report_from_bytes(byte_report, filename)

    def _build_filename(
        self,
        start_date: Optional[str],
        end_date: Optional[str],
        report_type: str = "xlsx",
    ) -> str:
        """Build a report filename based on date range and type."""
        if start_date and end_date:
            return f"ExpenseReport_{start_date}_{end_date}.xlsx"
        return f"ExpenseReport_FULL.xlsx"
