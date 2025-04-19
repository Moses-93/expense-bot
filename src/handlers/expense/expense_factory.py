import logging
from aiogram import Router
from src.services.api_client import APIClient
from src.handlers.expense import expense_handler
from .expense_router import ExpenseRouter


logger = logging.getLogger(__name__)


class ExpenseFactory:

    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def _create_handlers(self):
        create_handler = expense_handler.ExpenseCreateHandler(self.api_client)
        report_handler = expense_handler.ExpenseGetReportHandler(self.api_client)
        update_handler = expense_handler.ExpenseUpdateHandler(self.api_client)
        delete_handler = expense_handler.ExpenseDeleteHandler(self.api_client)

        return create_handler, report_handler, update_handler, delete_handler

    def get_router(self) -> Router:
        create, report, update, delete = self._create_handlers()
        return ExpenseRouter(
            create_handler=create,
            report_handler=report,
            update_handler=update,
            delete_handler=delete,
        ).router
