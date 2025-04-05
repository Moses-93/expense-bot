import logging
from aiogram import Router
from src.services.api_client import APIClient
from src.handlers.expense.expense_factory import ExpenseFactory
from src.handlers.start import router

logger = logging.getLogger(__name__)


class HandlerFactory:
    def __init__(self):
        logger.debug("Initializing HandlerFactory")
        self.router = Router()
        self.api_client = APIClient("http://localhost:8000/api")
        self.expense_factory = ExpenseFactory(self.api_client)

    def get_router(self) -> Router:
        """Get the router for the handlers."""
        expense_router = self.expense_factory.get_router()
        self.router.include_router(expense_router)
        self.router.include_router(router)
        return self.router
