from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from bookt_domain.model.command_handlers import handle_tenant_registration
from bookt_domain.model.commands import RegisterTenant
from bookt_domain.model.tenant_registrar import TenantRegistrar

# where can this go? I assume in a conftest file
pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.repository = MagicMock()
    uow.repository.get_singleton = AsyncMock()
    uow.repository.save = AsyncMock()
    return uow


@pytest.mark.asyncio
async def test_register_new_tenant_is_success(mock_uow):
    mock_tenant_id = uuid4()
    mock_registrar = TenantRegistrar()
    mock_registrar.create(tenant_registrar_id=mock_tenant_id)
    mock_uow.repository.get_singleton.return_value = mock_registrar

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
    mock_uow.repository.save.assert_called_once_with(aggregate=mock_registrar)


@pytest.mark.asyncio
async def test_register_new_tenant_adds_id_to_registered_tenant_ids(mock_uow):
    mock_tenant_id = uuid4()
    mock_registrar = TenantRegistrar()
    mock_registrar.create(tenant_registrar_id=mock_tenant_id)
    mock_uow.repository.get_singleton.return_value = mock_registrar

    await handle_tenant_registration(
        unit_of_work=mock_uow,
        command=RegisterTenant(
            tenant_id=mock_tenant_id,
            tenant_name="Some Tenant Name",
            tenant_registration_email="email@example.com",
        ),
    )

    assert mock_tenant_id in mock_registrar.registered_tenant_ids


@pytest.mark.asyncio
async def test_register_many_new_tenants_adds_ids_to_registered_tenant_ids(mock_uow):
    mock_registrar = TenantRegistrar()
    mock_registrar.create(tenant_registrar_id=uuid4())
    mock_uow.repository.get_singleton.return_value = mock_registrar

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

        assert mock_tenant_id in mock_registrar.registered_tenant_ids

    assert len(mock_registrar.registered_tenant_ids) == 3
