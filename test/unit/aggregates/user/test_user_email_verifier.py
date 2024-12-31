from uuid import uuid4

import pytest

from bookt_domain.model.aggregates.user.user_email_verifier import (
    UserEmailVerificationKeyWasIncorrect,
    UserEmailVerifier,
)


@pytest.fixture
def mock_verifier():
    mock_user_id = uuid4()

    verifier = UserEmailVerifier()
    verifier.create(user_id=mock_user_id)

    return verifier, mock_user_id


def test_verifier_create_is_success(mock_verifier):
    verifier, mock_user_id = mock_verifier
    assert verifier.user_id == mock_user_id


def test_verifier_has_verification_key(mock_verifier):
    verifier, _ = mock_verifier
    assert verifier.verification_key is not None


def test_verifier_has_stream_id_in_verification_key(mock_verifier):
    verifier, _ = mock_verifier
    assert verifier.verification_key.split(".")[0] == str(verifier.id)


def test_verifier_is_not_verified_after_creation(mock_verifier):
    verifier, _ = mock_verifier
    assert verifier.is_verified is False


def test_verify_email_marks_email_as_verifier(mock_verifier):
    verifier, _ = mock_verifier
    assert verifier.is_verified is False
    verifier.verify_email(verification_key=verifier.verification_key)
    assert verifier.is_verified is True


def test_verify_email_with_incorrect_key_throws_exception(mock_verifier):
    verifier, _ = mock_verifier
    assert verifier.is_verified is False
    with pytest.raises(UserEmailVerificationKeyWasIncorrect):
        verifier.verify_email(verification_key="NOT KEY")
