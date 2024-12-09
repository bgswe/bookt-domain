from uuid import uuid4

from bookt_domain.model.tenant_registrar import TenantRegistrar


def test_registrar_create_is_success():
    registrar_id = uuid4()

    registrar = TenantRegistrar()
    registrar.create(tenant_registrar_id=registrar_id)

    assert registrar.id == registrar_id
    assert len(registrar.registered_tenant_ids) == 0


def test_register_tenant_adds_tenant_id_to_registered_tenant_ids():
    registrar_id = uuid4()

    registrar = TenantRegistrar()
    registrar.create(tenant_registrar_id=registrar_id)

    assert len(registrar.registered_tenant_ids) == 0

    mock_tenant_id = uuid4()
    registrar.register_tenant(
        tenant_id=mock_tenant_id,
        tenant_name="some tenant",
        tenant_email="email@example.com",
    )

    assert len(registrar.registered_tenant_ids) == 1
    assert mock_tenant_id in registrar.registered_tenant_ids
