from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from typing import Tuple
from src.services.expense.expense_api_client import ExpenseAPIClient
from src.states.expenses import UpdateExpenseState
from src.services.expense.validators import ExpenseValidator


MESSAGES = {
    "start": "✏️ О, оновлюємо витрату! Обери зі списку запис, який хочеш змінити.",
    "set_new_name": "🔤 Тепер дай нову круту назву для цієї витрати. Можеш навіть додати емодзі! 😉",
    "set_new_date": "📅 Супер! Тепер вкажи нову дату у форматі РРРР-ММ-ДД. Наприклад: 2024-07-15",
    "success_update": "🎉 Вуаля! Витрату успішно оновлено! Тепер все виглядає супер!",
    "invalid_date": "🤔 Ой-ой, здається дата невірна. Спробуй ще раз у форматі РРРР-ММ-ДД, наприклад 2024-12-31",
    "not_found": "🤷‍♂️ Хмм... Схоже, тут пусто! Як щодо створити свою першу статтю витрат?",
    "error_update": "🔧 Щось пішло не так при оновленні. Не хвилюйся, це тимчасово! Спробуй ще раз за 5 хвилин."
}


class UpdateFSMService:

    def __init__(
        self, validator: ExpenseValidator, expense_api_client: ExpenseAPIClient
    ):
        self.validator = validator
        self.expense_api_client = expense_api_client

    async def start_update_expenses(
        self, user_id: int, state: FSMContext
    ) -> Tuple[str, InlineKeyboardMarkup]:
        expenses = await self.expense_api_client.get_expenses(user_id)
        await state.set_state(UpdateExpenseState.EXPENSE_ID)
        return (MESSAGES["start_update_expense"],)  # TODO: Add keyboard

    async def set_expense_id(self, expense_id: int, state: FSMContext):
        await state.set_data(id=expense_id)
        return MESSAGES["success_update"]

    async def set_new_name(self, name: str, state: FSMContext):
        await state.set_data(name=name)
        return MESSAGES["set_new_name"]

    async def set_new_date(self, user_id: int, date: str, state: FSMContext):
        if not await self.validator.is_valid_date(date):
            return MESSAGES["invalid_date"]
        await state.set_data(date=date)
        expense_data = await state.get_data()
        expense_id = expense_data.pop("id")
        return await self.expense_api_client.update_expense(
            user_id, expense_id, expense_data
        )
