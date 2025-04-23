ERROR_MESSAGES = {
    "invalid_date": "❌ Упс, щось не так з датою! Спробуй ще раз у форматі *ДД.ММ.РРРР*. Наприклад: 01.01.2025",
    "invalid_uah_amount": "❌ Упс, сума має бути числом (крапка замість коми). Давай ще раз: 100 або 50.25.",
    "invalid_title": "❌ Некоректна назва статті. Спробуйте вказати довшу назву.",
    "report_error": "😬 Ой-ой, звіт не вдалося створити! Але нічого страшного — спробуй ще раз трохи пізніше. Я вже працюю над виправленням! 💪",
    "not_found": "🤷‍♂️ Хмм... Схоже, тут пусто! Як щодо створити свою першу статтю витрат?",
    "no_changes": "🔕 Ви не змінили жодного поля. Витрату не оновлено.",
    "error_update": "🔧 Щось пішло не так при оновленні. Не хвилюйся, це тимчасово! Спробуй ще раз за 5 хвилин.",
    "error_delete": "🔧 Щось пішло не так при видаленні. Не хвилюйся, це тимчасово! Спробуй ще раз за 5 хвилин.",
}

GET_EXPENSE_MESSAGES = {
    "start": "📊 Генеруємо звіт! Введи *початкову дату* у форматі *ДД.ММ.РРРР*. Наприклад: 01.01.2025",
    "set_end_date": "➡️ Тепер вкажи *кінцеву дату*. Так само — *ДД.ММ.РРРР*. Наприклад: 01.01.2025",
    "success": "✨ Чудово! Звіт успішно згенеровано. Тепер можна аналізувати та планувати далі! 💪",
    "invalid_date": ERROR_MESSAGES["invalid_date"],
}

ADD_EXPENSE_MESSAGES = {
    "start": "🎉 Поїхали! Додаймо витрату. Напиши назву того, на що витратив(ла) гроші.",
    "set_date": "📅 Тепер вкажи дату у форматі *ДД.ММ.РРРР*. Наприклад: 01.01.2025. Можеш навіть взяти з майбутнього! 😉",
    "set_amount": "💸 Сума у гривнях (з копійками, якщо є). Наприклад: 150 або 75.50. Так-так, навіть дрібнички враховуємо!",
    "success_create": "✅ Супер! Витрату додано.\nНазва: {title}\nДата: {date}\nСума: {amount} грн.",
    "invalid_title": ERROR_MESSAGES["invalid_title"],
    "invalid_date": ERROR_MESSAGES["invalid_date"],
    "invalid_uah_amount": ERROR_MESSAGES["invalid_uah_amount"],
}

DELETE_EXPENSE_MESSAGES = {
    "start": "🗑️ Видаляємо витрату! Обери зі списку нижче те, що більше не актуальне.",
    "success_delete": "✨ Готово! Зміни успішно збережено. Все ідеально, як ти й хотів(ла)! 😊",
    "not_found": ERROR_MESSAGES["not_found"],
    "error_delete": ERROR_MESSAGES["error_delete"],
}

UPDATE_EXPENSE_MESSAGES = {
    "no_changes": ERROR_MESSAGES["no_changes"],
    "success_update": "✅ Витрату оновлено!\nНазва: {title}\nДата: {date}\nСума: {amount} грн.",
    "start": "🔄 Вибери витрату, яку хочеш змінити:",
    "invalid_title": ERROR_MESSAGES["invalid_title"],
    "invalid_date": ERROR_MESSAGES["invalid_date"],
    "invalid_uah_amount": ERROR_MESSAGES["invalid_uah_amount"],
    "steps": {
        "title": {
            "text": "📝 Введи нову назву витрати або натисни 'Пропустити'",
            "skip_callback": "skip_title",
        },
        "date": {
            "text": "📆 Введи нову дату у форматі DD.MM.YYYY або натисни 'Пропустити'",
            "skip_callback": "skip_date",
        },
        "amount": {
            "text": "💰 Введи нову суму в гривнях або натисни 'Пропустити'",
            "skip_callback": "skip_amount",
        },
    },
}
