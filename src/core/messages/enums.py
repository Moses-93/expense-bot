from enum import Enum, auto


class AddExpenseMessage(str, Enum):
    START = auto()
    SET_DATE = auto()
    SET_AMOUNT = auto()
    SUCCESS = auto()


class GetExpenseMessage(str, Enum):
    START_DATE = auto()
    END_DATE = auto()
    SUCCESS = auto()


class UpdateExpenseMessage(str, Enum):
    START = auto()
    SET_TITLE = auto()
    SET_DATE = auto()
    SET_AMOUNT = auto()
    SUCCESS = auto()


class DeleteExpenseMessage(str, Enum):
    START = auto()
    SUCCESS = auto()


class ErrorMessage(str, Enum):
    INVALID_TITLE = auto()
    INVALID_DATE = auto()
    INVALID_AMOUNT = auto()
    UPDATE_ERROR = auto()
    DELETE_ERROR = auto()
    REPORT_ERROR = auto()
    NOT_FOUND = auto()
    NO_CHANGES = auto()
