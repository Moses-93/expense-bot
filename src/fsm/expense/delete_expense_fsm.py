from typing import Tuple
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from src.services.expense.expense_api_client import ExpenseAPIClient
from src.states.expenses import DeleteExpenseState
from src.services.expense.validators import ExpenseValidator
from src.services.expense.expense_service import ExpenseReportService

MESSAGES = {
    "start": "🗑️ Так, видаляємо витрату! Обери зі списку нижче те, що більше не актуальне.",
    "success_update": "✨ Готово! Зміни успішно збережено. Все ідеально, як ти й хотів(ла)! 😊",
    "not_found": "🤷‍♂️ Хмм... Схоже, тут пусто! Як щодо створити свою першу статтю витрат?",
    "error_delete": "🔧 Щось пішло не так при видаленні. Не хвилюйся, це тимчасово! Спробуй ще раз за 5 хвилин.",
    "select_id": "❌ Видаляємо непотрібне! Вкажи ID статті:",
}


class DeleteFSMService:

    def __init__(
        self,
        validator: ExpenseValidator,
        api_client: ExpenseAPIClient,
        report_service: ExpenseReportService,
    ):
        self.api_client = api_client
        self.validator = validator
        self.report_service = report_service

    async def start_delete_expense(
        self, user_id: int, state: FSMContext
    ) -> Tuple[str, InlineKeyboardMarkup]:
        await state.clear()
        report = await self.report_service.get_expenses_report(
            user_id, all_expenses=True
        )
        if not report:
            await state.clear()
            return MESSAGES["not_found"], None
        await state.set_state(DeleteExpenseState.EXPENSE_ID)
        return MESSAGES["select_id"], report

    async def delete_expense(self, user_id: int, expense_id: int, state: FSMContext):
        await state.clear()
        await self.api_client.delete_expense(user_id, expense_id)
        return MESSAGES["success_update"]
