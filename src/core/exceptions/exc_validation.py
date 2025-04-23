class ValidationError(Exception):
    """The base class for validation errors"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidAmountError(ValidationError):
    pass


class InvalidNameError(ValidationError):
    pass


class InvalidDateError(ValidationError):
    pass
