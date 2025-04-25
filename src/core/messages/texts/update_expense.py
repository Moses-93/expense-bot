from src.core.messages.enums import UpdateExpenseMessage


MESSAGES = {
    UpdateExpenseMessage.SUCCESS: "✅ Витрату оновлено!\nНазва: {title}\nДата: {date}\nСума: {amount} грн.",
    UpdateExpenseMessage.START: "🔄 Вибери витрату, яку хочеш змінити:",
    UpdateExpenseMessage.SET_TITLE: "📝 Введи нову назву витрати або натисни 'Пропустити'",
    UpdateExpenseMessage.SET_DATE: "📆 Введи нову дату у форматі DD.MM.YYYY або натисни 'Пропустити'",
    UpdateExpenseMessage.SET_AMOUNT: "💰 Введи нову суму в гривнях або натисни 'Пропустити'",
}
