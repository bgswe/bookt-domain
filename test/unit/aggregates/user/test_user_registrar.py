from uuid import uuid4

import pytest

from bookt_domain.model.user_registrar import (
    TenantIDIsNotEligibleForUserRegistration,
    UserEmailHasAlreadyBeenRegistered,
    UserIDHasAlreadyBeenRegistered,
    UserRegistrar,
    UserRoles,
)


def test_registrar_create_is_success():
    registrar_id = uuid4()

    registrar = UserRegistrar()
    registrar.create(user_registrar_id=registrar_id)

    assert registrar.id == registrar_id
    assert len(registrar.eligible_tenant_ids) == 0
    assert len(registrar.created_user_ids) == 0
    assert len(registrar.created_user_emails) == 0


def test_add_eligible_tenant_id_is_success():
    registrar = UserRegistrar()
    registrar.create(user_registrar_id=uuid4())

    mock_tenant_id = uuid4()

    registrar.add_eligible_tenant_id(tenant_id=mock_tenant_id)

    assert mock_tenant_id in registrar.eligible_tenant_ids


def test_register_user_is_success():
    registrar = UserRegistrar()
    registrar.create(user_registrar_id=uuid4())

    mock_tenant_id = uuid4()
    registrar.add_eligible_tenant_id(tenant_id=mock_tenant_id)

    mock_user_id = uuid4()
    mock_email = "user@example.com"
    registrar.register_user(
        user_id=mock_user_id,
        email=mock_email,
        tenant_id=mock_tenant_id,
        roles=[UserRoles.TENANT_ADMIN],
    )

    assert mock_user_id in registrar.created_user_ids
    assert mock_email in registrar.created_user_emails


def test_register_user_errs_when_using_ineligible_tenant_id():
    registrar = UserRegistrar()
    registrar.create(user_registrar_id=uuid4())

    with pytest.raises(TenantIDIsNotEligibleForUserRegistration):
        registrar.register_user(
            email="user@example.com",
            tenant_id=uuid4(),  # ineligible ID
            roles=[UserRoles.TENANT_ADMIN],
        )


def test_register_user_errs_when_reusing_a_user_id():
    registrar = UserRegistrar()
    registrar.create(user_registrar_id=uuid4())

    mock_tenant_id = uuid4()
    registrar.add_eligible_tenant_id(tenant_id=mock_tenant_id)

    mock_user_id = uuid4()
    registrar.register_user(
        user_id=mock_user_id,
        email="email_1@example.com",
        tenant_id=mock_tenant_id,
        roles=[UserRoles.TENANT_ADMIN],
    )

    assert mock_user_id in registrar.created_user_ids

    # reuse ID to assert exception raised
    with pytest.raises(UserIDHasAlreadyBeenRegistered):
        registrar.register_user(
            user_id=mock_user_id,
            email="email_2@example.com",
            tenant_id=mock_tenant_id,
            roles=[UserRoles.TENANT_ADMIN],
        )


def test_register_user_errs_when_reusing_a_user_email():
    registrar = UserRegistrar()
    registrar.create(user_registrar_id=uuid4())

    mock_tenant_id = uuid4()
    registrar.add_eligible_tenant_id(tenant_id=mock_tenant_id)

    mock_email = "email@example.com"
    registrar.register_user(
        user_id=uuid4(),
        email=mock_email,
        tenant_id=mock_tenant_id,
        roles=[UserRoles.TENANT_ADMIN],
    )

    assert mock_email in registrar.created_user_emails

    # reuse ID to assert exception raised
    with pytest.raises(UserEmailHasAlreadyBeenRegistered):
        registrar.register_user(
            user_id=uuid4(),
            email=mock_email,
            tenant_id=mock_tenant_id,
            roles=[UserRoles.TENANT_ADMIN],
        )
