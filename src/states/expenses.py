from aiogram.fsm.state import State, StatesGroup


class AddExpenseStates(StatesGroup):
    """States for adding an expense."""

    TITLE = State()
    AMOUNT = State()
    DATE = State()


class GetExpensesReportStates(StatesGroup):
    """States for getting an expenses report."""

    START_DATE = State()
    END_DATE = State()


class DeleteExpenseStates(StatesGroup):

    EXPENSE_ID = State()


class UpdateExpenseStates(StatesGroup):

    EXPENSE_ID = State()
    TITLE = State()
    DATE = State()
    AMOUNT = State()


all_states = [
    *AddExpenseStates.__state_names__,
    *UpdateExpenseStates.__state_names__,
    *GetExpensesReportStates.__state_names__,
]
