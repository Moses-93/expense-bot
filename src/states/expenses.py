from aiogram.fsm.state import State, StatesGroup


class AddExpenseStates(StatesGroup):
    """States for adding an expense."""

    ADD_EXPENSE_NAME = State()
    ADD_EXPENSE_AMOUNT = State()
    ADD_EXPENSE_DATE = State()


class GetExpensesReportStates(StatesGroup):
    """States for getting an expenses report."""

    START_DATE = State()
    END_DATE = State()


class DeleteExpenseStates(StatesGroup):

    EXPENSE_ID = State()


class UpdateExpenseStates(StatesGroup):

    EXPENSE_ID = State()
    NAME = State()
    DATE = State()
    AMOUNT = State()
