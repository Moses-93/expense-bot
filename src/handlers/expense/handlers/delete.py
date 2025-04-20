import logging
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.keyboards.display_data_keyboard import DisplayData
from src.services.api_client import APIClient

from src.states.expenses import DeleteExpenseStates
from src.utils.message_manager import MessageManager
from src.services.expense import (
    expense_service as exp_service,
)
from src.handlers.expense.messages import DELETE_EXPENSE_MESSAGES


logger = logging.getLogger(__name__)


class ExpenseDeleteHandler:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.messages = MessageManager(DELETE_EXPENSE_MESSAGES)

    async def start(self, message: Message, state: FSMContext):
        await state.clear()
        expense_data = await exp_service.JSONExpenseReportService().execute(
            message.from_user.id, self.api_client
        )
        expense_keyboard = DisplayData.generate_keyboard(
            expense_data, ("name", "date", "uah_amount"), ("id",)
        )
        await state.set_state(DeleteExpenseStates.EXPENSE_ID)
        await message.answer(self.messages.get("start"), reply_markup=expense_keyboard)

    async def handle_delete_expense(self, callback: CallbackQuery, state: FSMContext):

        service = exp_service.ExpenseMutationService(
            self.api_client, callback.from_user.id
        )
        await service.delete(callback.data)

        await callback.message.answer(
            self.messages.get("success_delete"), parse_mode="Markdown"
        )
        await state.clear()
