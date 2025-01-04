from uuid import uuid4

import bcrypt
import pytest

from bookt_domain.model.aggregates.user.user_authenticator import (
    AuthenticationAttemptWithNoSetPassword,
    IncorrectPasswordProvided,
    UserAuthenticator,
)


@pytest.fixture
def authenticator() -> UserAuthenticator:
    authenticator = UserAuthenticator()
    authenticator.create(user_id=uuid4())
    return authenticator


@pytest.fixture
def mock_password_hash() -> str:
    salt = bcrypt.gensalt(rounds=4)  # minimize time spent generating in tests
    return bcrypt.hashpw(password="foobar".encode("utf-8"), salt=salt).decode("utf-8")


@pytest.fixture
def authenticator_w_password(authenticator, mock_password_hash) -> UserAuthenticator:
    authenticator.update_current_password_hash(password_hash=mock_password_hash)
    assert authenticator.password_hash == mock_password_hash
    return authenticator


def test_authenticator_create_is_success():
    mock_uuid = uuid4()
    authenticator = UserAuthenticator()
    authenticator.create(user_id=mock_uuid)
    assert getattr(authenticator, "id", None) is not None


def test_authenticate_without_set_password_raises_exception(authenticator):
    with pytest.raises(AuthenticationAttemptWithNoSetPassword):
        authenticator.authenticate(password="foobar")


def test_update_password_updates_stored_hash(authenticator, mock_password_hash):
    assert authenticator.password_hash is None
    authenticator.update_current_password_hash(password_hash=mock_password_hash)
    assert authenticator.password_hash == mock_password_hash


def test_authenticate_with_incorrect_password_raises_exception(
    authenticator_w_password,
):
    with pytest.raises(IncorrectPasswordProvided):
        authenticator_w_password.authenticate(password="foobaz")


def test_authenticate_with_correct_password_is_success(authenticator_w_password):
    authenticator_w_password.authenticate(password="foobar")
