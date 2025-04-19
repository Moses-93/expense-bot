from datetime import datetime
from typing import Optional


def date_validator(date_str: str) -> Optional[str]:
    """
    Validate if the given string represents a valid date in the specified format.

    Args:
        date_str (str): The date string to validate

    Returns:
        Optional[str]: The parsed date str in the format 'YYYY-MM-DD' if valid, None otherwise
    """
    try:
        return datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None


def amount_validator(amount: str) -> Optional[float]:
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


def name_validator(name: str) -> Optional[str]:
    try:
        return str(name) if len(str(name)) > 3 else None
    except ValueError:
        return None
