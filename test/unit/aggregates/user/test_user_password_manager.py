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


def test_user_set_password_is_success(password_manager):
    manager, _ = password_manager

    manager.set_password(
        key=manager.initial_password_key,
        password="PASSWORD",
    )


def test_user_set_password_key_is_invalid(password_manager):
    manager, _ = password_manager

    with pytest.raises(SetPasswordKeyWasInvalid):
        manager.set_password(key="OBVIOUSLY WRONG KEY", password="PASSWORD")


def test_set_password_adds_password_hash_to_password_history(password_manager):
    manager, _ = password_manager

    assert len(manager.password_history) == 0
    manager.set_password(
        key=manager.initial_password_key,
        password="some_password",
    )

    assert len(manager.password_history) == 1


def test_set_initial_password_sets_initial_key_to_none(password_manager):
    manager, _ = password_manager

    assert manager.initial_password_key is not None

    manager.set_password(
        key=manager.initial_password_key,
        password="some_password",
    )

    assert manager.initial_password_key is None
