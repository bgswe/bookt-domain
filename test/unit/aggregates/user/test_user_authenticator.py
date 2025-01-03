from uuid import UUID, uuid4

import pytest

from bookt_domain.model.aggregates.user.user_authenticator import (
    AuthenticationAttemptWithNoSetPassword,
    IncorrectPasswordProvided,
    UserAuthenticator,
)


@pytest.fixture
def mock_authenticator() -> tuple[UserAuthenticator, UUID]:
    mock_user_id = uuid4()

    authenticator = UserAuthenticator()
    authenticator.create(user_id=mock_user_id)

    return authenticator, mock_user_id


def test_authenticator_create_is_success(mock_authenticator):
    authenticator, mock_user_id = mock_authenticator
    assert authenticator.user_id == mock_user_id


def test_authenticate_without_set_password_raises_exception(mock_authenticator):
    authenticator, _ = mock_authenticator

    with pytest.raises(AuthenticationAttemptWithNoSetPassword):
        authenticator.authenticate(password="foobar")


def test_update_password_updates_stored_hash(mock_authenticator):
    authenticator, _ = mock_authenticator

    assert authenticator.password_hash is None

    mock_password_hash = "asdfna0nfa0we9f"
    authenticator.update_current_password_hash(password_hash=mock_password_hash)

    assert authenticator.password_hash == mock_password_hash


def test_authenticate_with_incorrect_password_raises_exception(mock_authenticator):
    authenticator, _ = mock_authenticator

    mock_password_hash = "asdfna0nfa0we9f"
    authenticator.update_current_password_hash(password_hash=mock_password_hash)

    assert authenticator.password_hash == mock_password_hash

    with pytest.raises(IncorrectPasswordProvided):
        authenticator.authenticate(password="foobar")
