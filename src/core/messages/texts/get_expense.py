from src.core.messages.enums import GetExpenseMessage


MESSAGES = {
    GetExpenseMessage.START_DATE: "📊 Генеруємо звіт! Введи *початкову дату* у форматі *ДД.ММ.РРРР*. Наприклад: 01.01.2025",
    GetExpenseMessage.END_DATE: "➡️ Тепер вкажи *кінцеву дату*. Так само — *ДД.ММ.РРРР*. Наприклад: 01.12.2025",
    GetExpenseMessage.SUCCESS: "✨ Чудово! Звіт успішно згенеровано. Тепер можна аналізувати та планувати далі! 💪",
}
