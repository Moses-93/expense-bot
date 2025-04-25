from src.core.messages.enums import AddExpenseMessage


MESSAGES = {
    AddExpenseMessage.START: "🎉 Поїхали! Додаймо витрату. Напиши назву того, на що витратив(ла) гроші.",
    AddExpenseMessage.SET_DATE: "📅 Тепер вкажи дату у форматі *ДД.ММ.РРРР*. Наприклад: 01.01.2025. Можеш навіть взяти з майбутнього! 😉",
    AddExpenseMessage.SET_AMOUNT: "💸 Сума у гривнях (з копійками, якщо є). Наприклад: 150 або 75.50. Так-так, навіть дрібнички враховуємо!",
    AddExpenseMessage.SUCCESS: "✅ Супер! Витрату додано.\nНазва: {title}\nДата: {date}\nСума: {amount} грн.",
}
