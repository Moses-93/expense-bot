class ExpenseError(Exception):
    def __init__(self, status_code: int, message: str = "Unexpected error"):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


class ExpenseNotFoundError(ExpenseError):
    pass


class ExpenseCreateError(ExpenseError):
    pass


class ExpenseUpdateError(ExpenseError):
    pass


class ExpenseDeleteError(ExpenseError):
    pass
