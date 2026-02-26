# tests/test_services.py
import pytest
from unittest.mock import MagicMock
from src.mi_app.services import UserService
from src.mi_app.models import User
from src.mi_app.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidUserDataError,
)


def test_create_user_success():
    """Verifica si la creacion de un usuario es exitosa"""
    mock_storage = MagicMock()
    mock_storage.load.return_value = []

    service = UserService(mock_storage)
    user = User(id=1, name="Leo", email="leo@test.com")

    service.create_user(user)

    mock_storage.save.assert_called_once()


def test_create_user_duplicate_id():
    """Verifica que se arroje un error si se crea un user con un id
    existente
    """

    mock_storage = MagicMock()

    mock_storage.load.return_value = [
        User(id=1, name="Existing", email="existing@test.com")
    ]

    service = UserService(mock_storage)
    user = User(id=1, name="Leo", email="leo@test.com")

    with pytest.raises(UserAlreadyExistsError):
        service.create_user(user)

    mock_storage.save.assert_not_called()


def test_create_user_invalid_data():
    """Verifica que se lance un error con datos invalidos de user"""
    mock_storage = MagicMock()
    service = UserService(mock_storage)

    user = User(id=1, name="", email="")

    with pytest.raises(InvalidUserDataError):
        service.create_user(user)


def test_get_user_not_found():
    """Verifica que se lance un error cuando se intente buscar user
    inexistente.
    """
    mock_storage = MagicMock()
    mock_storage.load.return_value = []

    service = UserService(mock_storage)

    with pytest.raises(UserNotFoundError):
        service.get_user(99)


def test_create_user_invalid_email():
    """Verifica que se lance un error con un email invalido"""
    mock_storage = MagicMock()
    service = UserService(mock_storage)

    user = User(id=1, name="Leo", email="invalid-email")

    with pytest.raises(InvalidUserDataError) as exec_info:
        service.create_user(user)

    assert "Invalid email address" in str(exec_info.value)
