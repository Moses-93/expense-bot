from datetime import datetime


class ExpenseValidator:

    def is_valid_date(self, date: str) -> bool:
        """
        Validate if the given string represents a valid date in YYYY-MM-DD format.

        Args:
            date (str): The date string to validate

        Returns:
            bool: True if date is valid, False otherwise
        """
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def is_valid_amount(self, amount: str) -> bool:
        """
        Validate if the given string represents a valid float number.

        Args:
            amount (str): The string to validate

        Returns:
            bool: True if amount is a valid float, False otherwise
        """
        try:
            float_value = float(amount)
            return float_value > 0
        except ValueError:
            return False
