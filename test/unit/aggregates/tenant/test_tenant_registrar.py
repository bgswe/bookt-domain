from uuid import uuid4

import pytest

from bookt_domain.model.aggregates.tenant.tenant_registrar import (
    TenantIDAlreadyRegistered,
    TenantRegistrar,
)


@pytest.fixture
def registrar() -> TenantRegistrar:
    registrar = TenantRegistrar()
    registrar.create(tenant_registrar_id=uuid4())
    return registrar


def test_registrar_create_is_success():
    registrar_id = uuid4()

    registrar = TenantRegistrar()
    registrar.create(tenant_registrar_id=registrar_id)

    assert registrar.id == registrar_id
    assert len(registrar.registered_tenant_ids) == 0


def test_register_tenant_adds_tenant_id_to_registered_tenant_ids(registrar):
    assert len(registrar.registered_tenant_ids) == 0

    mock_tenant_id = uuid4()
    registrar.register_tenant(
        tenant_id=mock_tenant_id,
        tenant_name="some tenant",
        tenant_email="email@example.com",
    )

    assert len(registrar.registered_tenant_ids) == 1
    assert mock_tenant_id in registrar.registered_tenant_ids


def test_tenant_registrar_raises_exception_on_tenant_id_already_registered(registrar):
    mock_tenant_id = uuid4()
    registrar.register_tenant(
        tenant_id=mock_tenant_id,
        tenant_name="some tenant",
        tenant_email="email@example.com",
    )

    assert len(registrar.registered_tenant_ids) == 1
    assert mock_tenant_id in registrar.registered_tenant_ids

    with pytest.raises(TenantIDAlreadyRegistered):
        registrar.register_tenant(
            tenant_id=mock_tenant_id,
            tenant_name="some alt tenant",
            tenant_email="alt_email@example.com",
        )
