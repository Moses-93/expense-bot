from typing import Tuple
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from src.services.expense.expense_api_client import ExpenseAPIClient
from src.states.expenses import DeleteExpenseState
from src.services.expense.validators import ExpenseValidator
from src.keyboards.display_data_keyboard import DisplayData


MESSAGES = {
    "start_delete_expense": "🗑️ Так, видаляємо витрату! Обери зі списку нижче те, що більше не актуальне.",
    "success_update": "✨ Готово! Зміни успішно збережено. Все ідеально, як ти й хотів(ла)! 😊",
}


class DeleteFSMService:

    def __init__(
        self, validator: ExpenseValidator, expense_api_client: ExpenseAPIClient
    ):
        self.validator = validator
        self.expense_api_client = expense_api_client

    async def start_delete_expense(
        self, user_id: int, state: FSMContext
    ) -> Tuple[str, InlineKeyboardMarkup]:
        expenses = await self.expense_api_client.get_expenses(user_id)
        await state.set_state(DeleteExpenseState.EXPENSE_ID)
        return (MESSAGES["start"], DisplayData.generate_keyboard(expenses, "name", "id"))

    async def delete_expense(self, user_id: int, expense_id: int, state: FSMContext):
        await state.clear()
        await self.expense_api_client.delete_expense(user_id, expense_id)
        return MESSAGES["success_update"]
