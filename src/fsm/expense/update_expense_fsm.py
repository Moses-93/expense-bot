from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from typing import Tuple
from src.services.expense.expense_api_client import ExpenseAPIClient
from src.states.expenses import UpdateExpenseState
from src.services.expense.validators import ExpenseValidator
from src.services.expense.expense_service import ExpenseReportService

MESSAGES = {
    "start": "✏️ О, оновлюємо витрату! Обери зі списку запис, який хочеш змінити.",
    "select_id": "🔍 Яку статтю редагуємо? Введи її ID:",
    "set_new_name": "🔤 Ось твоя стаття витрати:\nСтаття: {name}\nДата: {date}\nСума в UAH: {uah_amount}\n\nСума в USD: {usd_amount}\n\nТепер дай нову круту назву для цієї витрати. Можеш навіть додати емодзі! 😉",
    "set_new_date": "📅 Супер! Тепер вкажи нову дату у форматі *ДД.ММ.РРРР*. Наприклад: 01.01.2025",
    "success_update": "🎉 Вуаля! Витрату успішно оновлено! Тепер все виглядає супер!",
    "invalid_date": "🤔 Ой-ой, здається дата невірна. Спробуй ще раз у форматі *ДД.ММ.РРРР*, наприклад 01.01.2025",
    "not_found": "🤷‍♂️ Хмм... Схоже, тут пусто! Як щодо створити свою першу статтю витрат?",
    "error_update": "🔧 Щось пішло не так при оновленні. Не хвилюйся, це тимчасово! Спробуй ще раз за 5 хвилин.",
}


class UpdateFSMService:

    def __init__(
        self,
        validator: ExpenseValidator,
        expense_api_client: ExpenseAPIClient,
        report_service: ExpenseReportService,
    ):
        self.validator = validator
        self.expense_api_client = expense_api_client
        self.report_service = report_service

    async def start_update_expenses(
        self, user_id: int, state: FSMContext
    ) -> Tuple[str, InlineKeyboardMarkup]:
        await state.clear()
        report = await self.report_service.get_expenses_report(
            user_id, all_expenses=True
        )
        if not report:
            return MESSAGES["not_found"], None
        await state.set_state(UpdateExpenseState.EXPENSE_ID)
        return (MESSAGES["start"], report)

    async def set_expense_id(self, user_id: int, expense_id: int, state: FSMContext):
        await state.update_data(id=expense_id)
        expense = await self.expense_api_client.get_expense(user_id, expense_id)
        await state.set_state(UpdateExpenseState.NAME)
        return MESSAGES["set_new_name"].format(
            name=expense["name"],
            date=expense["date"],
            uah_amount=expense["uah_amount"],
            usd_amount=expense["usd_amount"],
        )

    async def set_new_name(self, name: str, state: FSMContext):
        await state.update_data(name=name)
        await state.set_state(UpdateExpenseState.DATE)
        return MESSAGES["set_new_date"]

    async def set_new_date(self, user_id: int, date: str, state: FSMContext):
        try:
            valid_date = self.validator.is_valid_date(date)
            if valid_date is None:
                await state.clear()
                return MESSAGES["invalid_date"]
            await state.update_data(date=valid_date)
            expense_data = await state.get_data()
            expense_id = expense_data.pop("id")
            response = await self.expense_api_client.update_expense(
                user_id, expense_id, expense_data
            )
            return MESSAGES["success_update"] if response else MESSAGES["error_update"]
        finally:
            await state.clear()
