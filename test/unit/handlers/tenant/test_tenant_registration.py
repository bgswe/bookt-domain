from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from bookt_domain.model.aggregates.tenant.tenant_registrar import TenantRegistrar
from bookt_domain.model.command_handlers import handle_tenant_registration
from bookt_domain.model.commands import RegisterTenant


@pytest.mark.asyncio
async def test_tenant_registration_handler_is_success(mock_uow, mock_tenant_registrar):
    mock_tenant_registrar.register_tenant = MagicMock()
    mock_uow.repository.get_singleton.return_value = mock_tenant_registrar

    mock_tenant_id = uuid4()
    mock_tenant_name = "Some Tenant Name"
    mock_tenant_email = "email@example.com"

    await handle_tenant_registration(
        unit_of_work=mock_uow,
        command=RegisterTenant(
            tenant_id=mock_tenant_id,
            tenant_name=mock_tenant_name,
            tenant_registration_email=mock_tenant_email,
        ),
    )

    mock_uow.repository.get_singleton.assert_called_once_with(
        aggregate_root_class=TenantRegistrar,
    )
    mock_tenant_registrar.register_tenant.assert_called_once_with(
        tenant_id=mock_tenant_id,
        tenant_name=mock_tenant_name,
        tenant_email=mock_tenant_email,
    )
    mock_uow.repository.save.assert_called_once_with(aggregate=mock_tenant_registrar)
