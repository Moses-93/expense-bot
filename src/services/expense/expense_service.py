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

    async def get(
        self, user_id: int, response_type: Literal["json", "bytes", "text"], url: str
    ):
        return await self.api_client.get(url, user_id, response_type=response_type)

    async def update(self, expense_id: int, data: dict) -> dict:
        return await self.api_client.patch(
            f"/expenses/{expense_id}", self.user_id, json=data
        )

    async def delete(self, expense_id: int) -> dict:
        return await self.api_client.delete(f"/expenses/{expense_id}", self.user_id)

    async def create(self, user_id: int, expense_data: ExpenseDTO):
        return await self.api_client.post("/expenses/", user_id, expense_data)


class ReportGeneratorService:
    def __init__(self, mutation_service: ExpenseMutationService):
        self.mutation_service = mutation_service

    async def generate_report(
        self, user_id: int, request_data: ExpenseReportRequestDTO
    ) -> ExpenseReportFile:
        url = ExpenseReportURLBuilder("xlsx", request_data).build_url()
        report_bytes = await self.mutation_service.get(user_id, "bytes", url)
        filename = self._generate_filename(request_data)
        return ExpenseReportFile(filename=filename, content=report_bytes)

    def _generate_filename(self, request_data: ExpenseReportRequestDTO) -> str:
        return f"ExpenseReport_{request_data.start_date}_{request_data.end_date}.xlsx"
