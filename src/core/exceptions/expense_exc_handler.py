import logging
from typing import Callable
from functools import wraps
from aiohttp import ClientResponseError
from . import expense_exc

logger = logging.getLogger(__name__)

exceptions = {
    "get": expense_exc.ExpenseNotFoundError,
    "get_report": expense_exc.ExpenseGetReportError,
    "create": expense_exc.ExpenseCreateError,
    "update": expense_exc.ExpenseUpdateError,
    "delete": expense_exc.ExpenseDeleteError,
    "default": expense_exc.ExpenseError,
}


def handle_client_error(operation: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ClientResponseError as e:
                logger.error(
                    f"Error during '{operation}'. status: {e.status}. message: {e.message}"
                )
                raise exceptions.get(operation, exceptions["default"])(
                    e.status, e.message
                )

        return wrapper

    return decorator
