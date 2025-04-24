from datetime import datetime
from src.core.exceptions.exc_validation import (
    InvalidAmountError,
    InvalidDateError,
    InvalidTitleError,
)
from src.core.messages import ERROR_MESSAGES


class ExpenseValidator:
    @staticmethod
    def validate_title(title: str) -> str:
        """
        Validates the given title string.

        Args:
            title (str): The title to validate.

        Returns:
            str: The validated title.

        Raises:
            InvalidTitleError: If the title is too short or invalid.
        """
        if len(title.strip()) <= 3:
            raise InvalidTitleError(ERROR_MESSAGES["invalid_title"])
        return title.strip()

    @staticmethod
    def validate_date(date_str: str) -> str:
        """
        Validates and formats the given date string.

        Args:
            date_str (str): The date string in 'DD.MM.YYYY' format.

        Returns:
            str: The date in 'YYYY-MM-DD' format.

        Raises:
            InvalidDateError: If the date format is invalid.
        """
        try:
            return datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%d")
        except ValueError:
            raise InvalidDateError(ERROR_MESSAGES["invalid_date"])

    @staticmethod
    def validate_amount(amount_str: str) -> float:
        """
        Validates and converts the given amount string to a positive float.

        Args:
            amount_str (str): The amount string to validate.

        Returns:
            float: The validated amount.

        Raises:
            InvalidAmountError: If the amount is not a positive number.
        """
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise InvalidAmountError(ERROR_MESSAGES["invalid_amount"])
            return amount
        except (ValueError, TypeError):
            raise InvalidAmountError(ERROR_MESSAGES["invalid_amount"])
