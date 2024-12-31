from unittest.mock import patch
from uuid import uuid4

import pytest

from bookt_domain.model.aggregates.tenant.tenant_registrar import TenantWasRegistered
from bookt_domain.model.event_handlers import create_tenant_email_verifier


@patch("bookt_domain.model.event_handlers.TenantEmailVerifier.create")
@pytest.mark.asyncio
async def test_create_tenant_email_verifier_for_tenant(mock_verifier_create, mock_uow):
    mock_registrar_id = uuid4()
    mock_tenant_id = uuid4()
    mock_tenant_name = "Some Tenant Name"
    mock_tenant_email = "Some Tenant Email"

    mock_event = TenantWasRegistered(
        stream_id=mock_registrar_id,
        tenant_id=mock_tenant_id,
        tenant_name=mock_tenant_name,
        tenant_email=mock_tenant_email,
    )

    await create_tenant_email_verifier(unit_of_work=mock_uow, event=mock_event)

    mock_verifier_create.assert_called_once_with(tenant_id=mock_tenant_id)
    mock_uow.repository.save.assert_called_once()
