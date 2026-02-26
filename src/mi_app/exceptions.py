class AppError(Exception):
    """Base class for all application-specific exceptions."""

    pass


class UserError(AppError):
    """Base class for user-related exceptions."""

    pass


class UserNotFoundError(UserError):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(f"User with id {user_id} not found")


class UserAlreadyExistsError(UserError):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(f"User with id {user_id} already exists")


class InvalidUserDataError(UserError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
