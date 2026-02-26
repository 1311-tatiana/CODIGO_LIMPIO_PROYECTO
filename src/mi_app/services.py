from .models import User
from .storage import Storage
from .exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidUserDataError,
)


class UserService:
    def __init__(self, storage: Storage):
        self.storage = storage

    def create_user(self, user: User) -> None:
        # check for required fields
        if user.id <= 0:
            raise InvalidUserDataError("User id must be a positive integer")

        if not user.name.strip():
            raise InvalidUserDataError("User name cannot be empty")

        if "@" not in user.email:
            raise InvalidUserDataError("Invalid email address")

        users = self.storage.load()

        # check for duplicate id
        if any(u.id == user.id for u in users):
            raise UserAlreadyExistsError(user.id)

        # finally add the user if all checks pass
        users.append(user)
        self.storage.save(users)

    def get_user(self, user_id: int) -> User:
        users = self.storage.load()
        for user in users:
            if user.id == user_id:
                return user
        raise UserNotFoundError(f"User {user_id} not found")

    def delete_user(self, user_id: int) -> None:
        users = self.storage.load()
        filtered = [u for u in users if u.id != user_id]

        if len(filtered) == len(users):
            raise UserNotFoundError(f"User {user_id} not found")

        self.storage.save(filtered)

