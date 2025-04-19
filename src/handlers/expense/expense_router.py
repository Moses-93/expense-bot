import logging
from aiogram import F, Router

from src.states import expenses
from src.handlers.expense import expense_handler

logger = logging.getLogger(__name__)


class ExpenseRouter:
    """Router for expense-related commands."""

    def __init__(
        self,
        create_handler: expense_handler.ExpenseCreateHandler,
        report_handler: expense_handler.ExpenseGetReportHandler,
        update_handler: expense_handler.ExpenseUpdateHandler,
        delete_handler: expense_handler.ExpenseDeleteHandler,
    ):
        self.router = Router()

        self._register_handlers(
            create_handler, report_handler, update_handler, delete_handler
        )

    def _register_handlers(
        self,
        create_handler: expense_handler.ExpenseCreateHandler,
        report_handler: expense_handler.ExpenseGetReportHandler,
        update_handler: expense_handler.ExpenseUpdateHandler,
        delete_handler: expense_handler.ExpenseDeleteHandler,
    ):
        self.router.message.register(
            create_handler.handle_add_expense,
            F.text == "➕ Додати витрату",
        )

        self.router.message.register(
            report_handler.handle_start,
            F.text == "📊 Мої витрати",
        )

        self.router.message.register(
            update_handler.handle_start_update_expense,
            F.text == "✏️ Редагувати витрату",
        )

        self.router.message.register(
            delete_handler.start,
            F.text == "❌ Видалити витрату",
        )

        self.router.message.register(
            create_handler.handle_set_expense_name,
            expenses.AddExpenseStates.ADD_EXPENSE_NAME,
        )

        self.router.message.register(
            create_handler.handle_set_expense_amount,
            expenses.AddExpenseStates.ADD_EXPENSE_AMOUNT,
        )

        self.router.message.register(
            create_handler.handle_set_expense_date,
            expenses.AddExpenseStates.ADD_EXPENSE_DATE,
        )

        self.router.message.register(
            report_handler.handle_set_start_date,
            expenses.GetExpensesReportStates.START_DATE,
        )

        self.router.message.register(
            report_handler.handle_set_end_date,
            expenses.GetExpensesReportStates.END_DATE,
        )

        self.router.callback_query.register(
            update_handler.set_expense_id, expenses.UpdateExpenseStates.EXPENSE_ID
        )

        self.router.message.register(
            update_handler.handle_set_name, expenses.UpdateExpenseStates.NAME
        )

        self.router.message.register(
            update_handler.handle_set_date, expenses.UpdateExpenseStates.DATE
        )

        self.router.message.register(
            update_handler.handle_set_amount, expenses.UpdateExpenseStates.AMOUNT
        )

        self.router.callback_query.register(
            update_handler.handle_skip, F.data.startswith("skip_")
        )

        self.router.callback_query.register(
            delete_handler.handle_delete_expense,
            expenses.DeleteExpenseStates.EXPENSE_ID,
        )
