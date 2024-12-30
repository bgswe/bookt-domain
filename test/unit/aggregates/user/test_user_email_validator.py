from uuid import uuid4

import pytest

from bookt_domain.model.aggregates.user.user_email_validator import (
    UserEmailValidationKeyWasIncorrect,
    UserEmailValidator,
)


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


def test_validate_email_marks_email_as_validated(mock_validator):
    validator, _ = mock_validator
    assert validator.is_validated is False
    validator.validate_email(validation_key=validator.validation_key)
    assert validator.is_validated is True


def test_validate_email_with_incorrect_key_throws_exception(mock_validator):
    validator, _ = mock_validator
    assert validator.is_validated is False
    with pytest.raises(UserEmailValidationKeyWasIncorrect):
        validator.validate_email(validation_key="NOT KEY")
