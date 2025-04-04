from aiogram.fsm.state import State, StatesGroup


class AddExpenseStates(StatesGroup):
    """States for adding an expense."""

    ADD_EXPENSE_NAME = State()
    ADD_EXPENSE_AMOUNT = State()
    ADD_EXPENSE_DATE = State()


class GetExpensesReportStates(StatesGroup):
    """States for getting an expenses report."""

    START_DATE = State()
    AND_DATE = State()
