from uuid import uuid4

import pytest

from bookt_domain.model.user_email_validator import UserEmailValidator


@pytest.fixture
def mock_validator():
    mock_user_id = uuid4()

    validator = UserEmailValidator()
    validator.create(user_id=mock_user_id)

    return validator, mock_user_id


def test_validator_create_is_success(mock_validator):
    validator, mock_user_id = mock_validator
    assert validator.user_id == mock_user_id


def test_validator_has_validation_key(mock_validator):
    validator, _ = mock_validator
    assert validator.validation_key is not None


def test_validator_has_stream_id_in_validation_key(mock_validator):
    validator, _ = mock_validator
    assert validator.validation_key.split(".")[0] == str(validator.id)


def test_validator_is_not_valid_after_creation(mock_validator):
    validator, _ = mock_validator
    assert validator.is_validated is False
