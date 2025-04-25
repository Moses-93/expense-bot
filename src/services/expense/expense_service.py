import logging
from typing import Optional, Dict, List, Literal
from yarl import URL

from src.services.api_client import APIClient
from src.models.expense_dto import (
    ExpenseDTO,
    ExpenseReportRequestDTO,
    UpdateExpenseDTO,
    ExpenseReportFile,
)

logger = logging.getLogger(__name__)


class ExpenseReportURLBuilder:
    def __init__(
        self,
        report_type: Literal["json", "xlsx"],
        request_data: Optional[ExpenseReportRequestDTO] = None,
    ):
        self.report_type = report_type
        self.request_data = request_data

    def _build_query_params(self) -> Dict:
        if self.request_data:
            return {
                "report_type": self.report_type,
                "start_date": self.request_data.start_date.isoformat(),
                "end_date": self.request_data.end_date.isoformat(),
            }
        return {
            "report_type": self.report_type,
            "all_expenses": "true",
        }

    def build_url(self) -> str:
        base_url = "/expenses/report/"
        return str(URL(base_url).with_query(self._build_query_params(report_type)))

    @abstractmethod
    async def execute(self, user_id: int, api_client: APIClient): ...


class JSONExpenseReportService(BaseExpenseReportService):
    def __init__(self, start_date=None, end_date=None):
        super().__init__(start_date, end_date)

    async def execute(self, user_id: int, api_client: APIClient) -> List[Dict]:
        self._validate_dates()
        url = self._build_url("json")
        return await api_client.get(url, user_id)


class FileExpenseReportService(BaseExpenseReportService):
    def __init__(self, report_type: str, start_date=None, end_date=None):
        super().__init__(start_date, end_date)
        self.report_type = report_type

    async def execute(self, user_id: int, api_client: APIClient) -> BufferedInputFile:
        self._validate_dates()
        url = self._build_url(self.report_type)
        byte_data = await api_client.get(url, user_id, response_type="bytes")
        return BufferedInputFile(byte_data, filename=self._build_filename())

    def _build_filename(self) -> str:
        if self.start_date and self.end_date:
            return f"ExpenseReport_{self.start_date}_{self.end_date}.{self.report_type}"
        return f"ExpenseReport_FULL.{self.report_type}"


class ExpenseMutationService:
    def __init__(self, api_client: APIClient, user_id: int):
        self.api_client = api_client
        self.user_id = user_id

    async def update(self, expense_id: int, data: dict) -> dict:
        return await self.api_client.patch(
            f"/expenses/{expense_id}", self.user_id, json=data
        )

    async def delete(self, expense_id: int) -> dict:
        return await self.api_client.delete(f"/expenses/{expense_id}", self.user_id)

    async def create(self, expense_data: Dict):
        return await self.api_client.post("/expenses/", self.user_id, expense_data)
