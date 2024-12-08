from uuid import uuid4

import pytest

from bookt_domain.model.command_handlers import handle_tenant_registration
from bookt_domain.model.commands import RegisterTenant
from bookt_domain.model.tenant_registrar import TenantRegistrar


@pytest.mark.asyncio
async def test_register_new_tenant_is_success(mock_uow, mock_tenant_registrar):
    mock_uow.repository.get_singleton.return_value = mock_tenant_registrar
    mock_tenant_id = uuid4()

    await handle_tenant_registration(
        unit_of_work=mock_uow,
        command=RegisterTenant(
            tenant_id=mock_tenant_id,
            tenant_name="Some Tenant Name",
            tenant_registration_email="email@example.com",
        ),
    )

    mock_uow.repository.get_singleton.assert_called_once_with(
        aggregate_root_class=TenantRegistrar
    )
    mock_uow.repository.save.assert_called_once_with(aggregate=mock_tenant_registrar)


@pytest.mark.asyncio
async def test_register_new_tenant_adds_id_to_registered_tenant_ids(
    mock_uow, mock_tenant_registrar
):
    mock_uow.repository.get_singleton.return_value = mock_tenant_registrar
    mock_tenant_id = uuid4()

    await handle_tenant_registration(
        unit_of_work=mock_uow,
        command=RegisterTenant(
            tenant_id=mock_tenant_id,
            tenant_name="Some Tenant Name",
            tenant_registration_email="email@example.com",
        ),
    )

    assert mock_tenant_id in mock_tenant_registrar.registered_tenant_ids


@pytest.mark.asyncio
async def test_register_many_new_tenants_adds_ids_to_registered_tenant_ids(
    mock_uow, mock_tenant_registrar
):
    mock_uow.repository.get_singleton.return_value = mock_tenant_registrar
    mock_tenant_id = uuid4()

    for _ in range(3):
        mock_tenant_id = uuid4()

        await handle_tenant_registration(
            unit_of_work=mock_uow,
            command=RegisterTenant(
                tenant_id=mock_tenant_id,
                tenant_name="Some Tenant Name",
                tenant_registration_email="email@example.com",
            ),
        )

        assert mock_tenant_id in mock_tenant_registrar.registered_tenant_ids

    assert len(mock_tenant_registrar.registered_tenant_ids) == 3
