import logging
from aiogram import Router
from src.services.api_client import APIClient
from src.handlers.expense import handlers
from .expense_router import ExpenseRouter
from src.utils.message_provider import MessageProvider
from src.core.messages.texts import (
    add_expense,
    delete_expense,
    get_expense,
    update_expense,
    error_message,
)
from src.services.expense import expense_service as exp_service

logger = logging.getLogger(__name__)


class ExpenseFactory:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def _build_mutation_service(self):
        return exp_service.ExpenseMutationService(self.api_client)

    def _build_keyboard_builder(self, mutation_service):
        return exp_service.ExpenseKeyboardBuilder(mutation_service)

    def _build_report_service(self, mutation_service):
        return exp_service.ReportGeneratorService(mutation_service)

    def _build_message_providers(self):
        return {
            "add": MessageProvider(add_expense.MESSAGES),
            "get": MessageProvider(get_expense.MESSAGES),
            "update": MessageProvider(update_expense.MESSAGES),
            "delete": MessageProvider(delete_expense.MESSAGES),
            "error": MessageProvider(error_message.ERROR_MESSAGES),
        }

    def _build_handlers(self):
        mutation_service = self._build_mutation_service()
        keyboard_builder = self._build_keyboard_builder(mutation_service)
        report_service = self._build_report_service(mutation_service)
        messages = self._build_message_providers()

        create_handler = handlers.create.ExpenseCreateHandler(
            messages["add"], mutation_service
        )
        report_handler = handlers.get.ExpenseGetReportHandler(
            report_service, messages["get"]
        )
        update_handler = handlers.update.ExpenseUpdateHandler(
            mutation_service, keyboard_builder, messages["update"]
        )
        delete_handler = handlers.delete.ExpenseDeleteHandler(
            mutation_service, messages["delete"]
        )
        error_handler = handlers.errors.ValidationErrorHandler(messages["error"])

        return (
            create_handler,
            report_handler,
            update_handler,
            delete_handler,
            error_handler,
        )

    def get_router(self) -> Router:
        create, report, update, delete, error = self._build_handlers()
        return ExpenseRouter(
            create_handler=create,
            report_handler=report,
            update_handler=update,
            delete_handler=delete,
            error_handler=error,
        ).router
