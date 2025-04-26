import logging
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Dict, Union
from src.core.exceptions import expense_exc

logger = logging.getLogger(__name__)


async def send_response(event: Union[Message, CallbackQuery], message: str):
    if isinstance(event, CallbackQuery):
        await event.message.answer(text=message)
    elif isinstance(event, Message):
        await event.answer(text=message)


class ErrorHandlingMiddleware(BaseMiddleware):

    async def __call__(self, handler, event: Union[Message, CallbackQuery], data: Dict):
        try:
            return await handler(event, data)
        except expense_exc.ExpenseCreateError as e:
            await send_response(event, e.message)
        except expense_exc.ExpenseDeleteError as e:
            await send_response(event, e.message)
        except expense_exc.ExpenseNotFoundError as e:
            await send_response(event, e.message)
        except expense_exc.ExpenseUpdateError as e:
            await send_response(event, e.message)
        except expense_exc.ExpenseError as e:
            await send_response(event, e.message)
