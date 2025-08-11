class UserAlreadyExistsError(Exception):
    """Raised when trying to create a user that already exists"""

    def __init__(self, name: str) -> None:
        self.name = name


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid"""

    def __init__(self, name: str) -> None:
        self.name = name


class UserNotFoundError(Exception):
    """Raised when user is not found"""

    def __init__(self, name: str) -> None:
        self.name = name
