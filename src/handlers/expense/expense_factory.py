import logging
from aiogram import Router
from src.handlers.expense import expense_handler
from src.services.expense.expense_api_client import ExpenseAPIClient
from .expense_router import ExpenseRouter
from src.services.api_client import APIClient
from src.fsm.expense.fsm_factory import ExpenseFSMFactory
from src.services.expense.validators import ExpenseValidator
from src.services.expense.expense_service import ExpenseReportService


logger = logging.getLogger(__name__)


class ExpenseFactory:
    def __init__(self, api_client: APIClient):
        logger.debug("Initializing ExpenseFactory")
        self.api_client = api_client
        self._init_services()

    def _init_services(self):
        self.expense_api_client = ExpenseAPIClient(self.api_client)
        self.validator = ExpenseValidator()
        self.report_service = ExpenseReportService(self.expense_api_client)
        self.fsm_factory = ExpenseFSMFactory(
            self.validator,
            self.expense_api_client,
            self.report_service,
        )

    def _create_handlers(self):
        create_handler = expense_handler.ExpenseCreateHandler(
            fsm_service=self.fsm_factory.create_add_fsm_service()
        )
        report_handler = expense_handler.ExpenseGetReportHandler(
            fsm_service=self.fsm_factory.create_report_fsm_service()
        )
        update_handler = expense_handler.ExpenseUpdateHandler(
            fsm_service=self.fsm_factory.create_update_fsm_service()
        )
        delete_handler = expense_handler.ExpenseDeleteHandler(
            fsm_service=self.fsm_factory.create_delete_fsm_service()
        )

        return create_handler, report_handler, update_handler, delete_handler

    def get_router(self) -> Router:
        create, report, update, delete = self._create_handlers()
        return ExpenseRouter(
            create_handler=create,
            report_handler=report,
            update_handler=update,
            delete_handler=delete,
        ).router
