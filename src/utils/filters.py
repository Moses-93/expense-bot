import logging
from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Union, Dict
from src.utils.expense_validators import ExpenseValidator
from src.core.exceptions.exc_validation import (
    InvalidAmountError,
    InvalidDateError,
    InvalidTitleError,
)


logger = logging.getLogger(__name__)


class AmountValidatorFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, float]]:
        try:
            amount = ExpenseValidator.validate_amount(message.text)
            return {"amount": amount}
        except InvalidAmountError:
            return False


class DateValidatorFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, str]]:
        try:
            date = ExpenseValidator.validate_date(message.text)
            logger.debug(f"{date=}")

            return {"date": date}
        except InvalidDateError:
            return False


class TitleValidatorFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, str]]:
        try:
            title = ExpenseValidator.validate_title(message.text)
            return {"title": title}
        except InvalidTitleError:
            return False
