from uuid import uuid4

import pytest

from bookt_domain.model.aggregates.user.user_email_validator import UserEmailValidator
from bookt_domain.model.aggregates.user.user_password_manager import UserPasswordManager


@pytest.fixture
def mock_validator():
    mock_user_id = uuid4()

    validator = UserEmailValidator()
    validator.create(user_id=mock_user_id)

    return validator, mock_user_id


def test_user_password_manager_create():
    mock_user_id = uuid4()

    password_manager = UserPasswordManager()
    password_manager.create(
        user_id=mock_user_id,
    )

    assert password_manager.user_id == mock_user_id
    assert password_manager.hashed_password is None
