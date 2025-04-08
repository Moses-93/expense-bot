from aiogram.fsm.context import FSMContext
from src.states.expenses import AddExpenseStates
from src.services.expense.expense_api_client import ExpenseAPIClient
from src.services.expense.validators import ExpenseValidator


MESSAGES = {
    "start_add_expense": "🎉 Поїхали! Давай додамо витрату. Напиши назву того, на що витратив(ла) гроші.",
    "set_date": "📅 Тепер вкажи дату у форматі *ДД.ММ.РРРР*. Наприклад: 01.01.2025. Можеш навіть взяти з майбутнього! 😉",
    "set_amount": "💸 Сума у гривнях (з копійками, якщо є). Наприклад: 150 або 75.50. Так-так, навіть дрібнички враховуємо!",
    "success_create_expense": "✅ Супер! Витрату додано. Можеш перевірити, чи не забув(ла) щось? 😊",
    "invalid_date": "❌ Ой, щось не так з датою! Спробуй ще раз у форматі *ДД.ММ.РРРР*. Наприклад: 01.01.2025.",
    "invalid_amount": "❌ Упс, сума має бути числом (крапка замість коми). Давай ще раз: 100 або 50.25.",
}


class AddExpenseFSMService:
    def __init__(
        self, validator: ExpenseValidator, expense_api_client: ExpenseAPIClient
    ):
        self.validator = validator
        self.expense_api_client = expense_api_client

    async def start(self, state: FSMContext):
        await state.clear()
        await state.set_state(AddExpenseStates.ADD_EXPENSE_NAME)
        return MESSAGES["start_add_expense"]

    async def set_name(self, state: FSMContext, name: str) -> str:
        await state.update_data(name=name)
        await state.set_state(AddExpenseStates.ADD_EXPENSE_DATE)
        return MESSAGES["set_date"]

    async def set_date(self, state: FSMContext, date: str):
        valid_date = self.validator.is_valid_date(date)
        if valid_date is None:
            await state.clear()
            return MESSAGES["invalid_date"]

        await state.update_data(date=valid_date)
        await state.set_state(AddExpenseStates.ADD_EXPENSE_AMOUNT)
        return MESSAGES["set_amount"]

    async def set_amount(self, state: FSMContext, user_id: int, amount: str):
        valid_amount = self.validator.is_valid_amount(amount)
        if valid_amount is None:
            await state.clear()
            return MESSAGES["invalid_amount"]

        data = await state.get_data()
        data["amount"] = valid_amount

        created_expense = await self.expense_api_client.create_expense(
            user_id=user_id, expense_data=data
        )
        if created_expense:
            return MESSAGES["success_create_expense"]
        await state.clear()
