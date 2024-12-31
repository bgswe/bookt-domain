from unittest.mock import MagicMock

import pytest

from bookt_domain.model.aggregates.user.user_email_verifier import UserEmailVerifier
from bookt_domain.model.command_handlers import handle_verify_user_email
from bookt_domain.model.commands import VerifyUserEmail


@pytest.mark.asyncio
async def test_user_email_verification_correctly_gets_verifier_id_from_key(mock_uow):
    mock_verifier_id = "MOCK_VERIFIER_ID"
    mock_random_key = "MOCK_RANDOM_KEY"

    mock_command = VerifyUserEmail(
        verification_key=f"{mock_verifier_id}.{mock_random_key}",
    )

    await handle_verify_user_email(
        unit_of_work=mock_uow,
        command=mock_command,
    )

    mock_uow.repository.get.assert_called_once_with(
        id=mock_verifier_id,
        aggregate_root_class=UserEmailVerifier,
    )


@pytest.mark.asyncio
async def test_user_email_verification_correctly_gets_random_key_from_verifier_key(
    make_mock_uow,
):
    mock_verifier = MagicMock()
    mock_uow = make_mock_uow(get_return_value=mock_verifier)

    mock_verifier_id = "MOCK_VERIFIER_ID"
    mock_random_key = "MOCK_RANDOM_KEY"

    mock_command = VerifyUserEmail(
        verification_key=f"{mock_verifier_id}.{mock_random_key}",
    )

    await handle_verify_user_email(
        unit_of_work=mock_uow,
        command=mock_command,
    )

    mock_verifier.verify_email.assert_called_once_with(
        verification_key=f"{mock_verifier_id}.{mock_random_key}",
    )
