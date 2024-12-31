from uuid import uuid4

import pytest

from bookt_domain.model.aggregates.user.user_password_manager import (
    SetPasswordKeyWasInvalid,
    UserPasswordManager,
)


@pytest.fixture
def password_manager():
    mock_user_id = uuid4()

    manager = UserPasswordManager()
    manager.create(user_id=mock_user_id)

    return manager, mock_user_id


def test_user_password_manager_create():
    mock_user_id = uuid4()

    password_manager = UserPasswordManager()
    password_manager.create(
        user_id=mock_user_id,
    )

    assert password_manager.user_id == mock_user_id
    assert password_manager.hashed_password is None


def test_user_set_password_is_success(password_manager):
    manager, _ = password_manager

    assert manager.hashed_password is None

    manager.set_password(
        key=manager.initial_password_key,
        password="PASSWORD",
    )


def test_user_set_password_key_is_invalid(password_manager):
    manager, _ = password_manager

    assert manager.hashed_password is None

    with pytest.raises(SetPasswordKeyWasInvalid):
        manager.set_password(key="OBVIOUSLY WRONG KEY", password="PASSWORD")
