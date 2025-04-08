from datetime import datetime, date
from typing import Optional


class ExpenseValidator:

    def is_valid_date(self, date_str: str) -> Optional[date]:
        """
        Validate if the given string represents a valid date in the specified format.

        Args:
            date_str (str): The date string to validate

        Returns:
            Optional[date]: The parsed date object if valid, None otherwise
        """
        try:
            return datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            return None

    def is_valid_amount(self, amount: str) -> Optional[float]:
        """
        Validate if the given string represents a valid positive float number.

        Args:
            amount (str): The string to validate

        Returns:
            Optional[float]: The float value if valid and positive, None otherwise
        """
        try:
            return float(amount) if float(amount) > 0 else None
        except (ValueError, TypeError):
            return None
