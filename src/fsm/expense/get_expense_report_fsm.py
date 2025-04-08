from aiogram.fsm.context import FSMContext
from src.states.expenses import GetExpensesReportStates
from src.services.expense.expense_service import ExpenseReportService
from src.services.expense.validators import ExpenseValidator


MESSAGES = {
    "start": "📊 Генеруємо звіт! Введи *початкову дату* у форматі *ДД.ММ.РРРР*. Наприклад: 01.01.2025",
    "set_end_date": "➡️ Тепер вкажи *кінцеву дату*. Так само — *ДД.ММ.РРРР*. Наприклад: 01.01.2025",
    "invalid_date": "❌ Упс, щось не так з датою! Спробуй ще раз у форматі *ДД.ММ.РРРР*. Наприклад: 01.01.2025",
    "success": "✨ Чудово! Звіт успішно згенеровано. Тепер можна аналізувати та планувати далі! 💪",
    "report_error": "😬 Ой-ой, звіт не вдалося створити! Але нічого страшного — спробуй ще раз трохи пізніше. Я вже працюю над виправленням! 💪",
}


class GetReportFSMService:
    def __init__(
        self, validator: ExpenseValidator, expense_report_service: ExpenseReportService
    ):
        self.validator = validator
        self.expense_report_service = expense_report_service

    async def start(self, state: FSMContext):
        await state.clear()
        await state.set_state(GetExpensesReportStates.START_DATE)
        return MESSAGES["start"]

    async def set_start_date(self, start_date: str, state: FSMContext):
        valid_date = self.validator.is_valid_date(start_date)
        if valid_date is None:
            await state.clear()
            return MESSAGES["invalid_date"]
        await state.update_data(start_date=start_date)
        await state.set_state(GetExpensesReportStates.END_DATE)
        return MESSAGES["set_end_date"]

    async def set_end_date(self, user_id: int, end_date: str, state: FSMContext):
        valid_date = self.validator.is_valid_date(end_date)
        if valid_date is None:
            await state.clear()
            return MESSAGES["invalid_date"], None
        data = await state.get_data()
        report = await self.expense_report_service.get_expenses_report(
            user_id, data["start_date"], data["end_date"]
        )
        return MESSAGES["success"], (report if report else MESSAGES["report_error"])
