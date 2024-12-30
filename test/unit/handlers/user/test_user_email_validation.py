from unittest.mock import MagicMock

import pytest

from bookt_domain.model.aggregates.user.user_email_validator import UserEmailValidator
from bookt_domain.model.command_handlers import handle_validate_user_email
from bookt_domain.model.commands import ValidateUserEmail


@pytest.mark.asyncio
async def test_user_email_validation_correctly_gets_validator_id_from_key(mock_uow):
    mock_validator_id = "MOCK_VALIDATOR_ID"
    mock_random_key = "MOCK_RANDOM_KEY"

    mock_command = ValidateUserEmail(
        validation_key=f"{mock_validator_id}.{mock_random_key}",
    )

    await handle_validate_user_email(
        unit_of_work=mock_uow,
        command=mock_command,
    )

    mock_uow.repository.get.assert_called_once_with(
        id=mock_validator_id,
        aggregate_root_class=UserEmailValidator,
    )


@pytest.mark.asyncio
async def test_user_email_validation_correctly_gets_random_key_from_validator_key(
    make_mock_uow,
):
    mock_validator = MagicMock()
    mock_uow = make_mock_uow(get_return_value=mock_validator)

    mock_validator_id = "MOCK_VALIDATOR_ID"
    mock_random_key = "MOCK_RANDOM_KEY"

    mock_command = ValidateUserEmail(
        validation_key=f"{mock_validator_id}.{mock_random_key}",
    )

    await handle_validate_user_email(
        unit_of_work=mock_uow,
        command=mock_command,
    )

    mock_validator.validate_email.assert_called_once_with(
        validation_key=f"{mock_validator_id}.{mock_random_key}",
    )
