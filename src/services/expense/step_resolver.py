from src.states import expenses

STEP_FIELD_MAPPING = {
    expenses.UpdateExpenseStates.NAME: "name",
    expenses.UpdateExpenseStates.DATE: "date",
    expenses.UpdateExpenseStates.AMOUNT: "uah_amount",
}


def get_field_from_state(state: str) -> str:
    return STEP_FIELD_MAPPING.get(state, "")


def next_step(current_state: str):
    steps = list(STEP_FIELD_MAPPING.keys())
    try:
        index = steps.index(current_state)
        return steps[index + 1]
    except (ValueError, IndexError):
        return None
