import logging
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Dict, Union
from src.core.exceptions import exc_validation

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
        except exc_validation.InvalidAmountError as e:
            await send_response(event, e.message)
        except exc_validation.InvalidDateError as e:
            await send_response(event, e.message)
        except exc_validation.InvalidTitleError as e:
            await send_response(event, e.message)
