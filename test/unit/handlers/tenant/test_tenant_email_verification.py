from unittest.mock import MagicMock

import pytest

from bookt_domain.model.aggregates.tenant.tenant_email_verifier import (
    TenantEmailVerifier,
)
from bookt_domain.model.command_handlers import handle_verify_tenant_email
from bookt_domain.model.commands import VerifyTenantEmail


@pytest.mark.asyncio
async def test_tenant_email_verification_correctly_gets_verification_id_from_key(
    mock_uow,
):
    mock_verifier_id = "MOCK_VERIFIER_ID"
    mock_random_key = "MOCK_RANDOM_KEY"

    mock_command = VerifyTenantEmail(
        verification_key=f"{mock_verifier_id}.{mock_random_key}",
    )

    await handle_verify_tenant_email(
        unit_of_work=mock_uow,
        command=mock_command,
    )

    mock_uow.repository.get.assert_called_once_with(
        id=mock_verifier_id,
        aggregate_root_class=TenantEmailVerifier,
    )


@pytest.mark.asyncio
async def test_tenant_email_verification_correctly_gets_random_key_from_verification_key(
    make_mock_uow,
):
    mock_verifier = MagicMock()
    mock_uow = make_mock_uow(get_return_value=mock_verifier)

    mock_verifier_id = "MOCK_VERIFICATION_ID"
    mock_random_key = "MOCK_RANDOM_KEY"

    mock_command = VerifyTenantEmail(
        verification_key=f"{mock_verifier_id}.{mock_random_key}",
    )

    await handle_verify_tenant_email(
        unit_of_work=mock_uow,
        command=mock_command,
    )

    mock_verifier.verify_email.assert_called_once_with(
        verification_key=f"{mock_verifier_id}.{mock_random_key}",
    )
