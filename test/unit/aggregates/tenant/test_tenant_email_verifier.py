from unittest.mock import patch
from uuid import uuid4

import pytest

from bookt_domain.model.aggregates.tenant.tenant_email_verifier import (
    TenantEmailVerificationKeyWasIncorrect,
    TenantEmailVerifier,
)


def test_verifier_create_is_success():
    mock_tenant_id = uuid4()

    verifier = TenantEmailVerifier()
    verifier.create(tenant_id=mock_tenant_id)

    assert verifier.tenant_id == mock_tenant_id


def test_verifier_is_not_verified_after_creation():
    registrar = TenantEmailVerifier()
    registrar.create(tenant_id=uuid4())

    assert not registrar.is_verified


@patch("bookt_domain.model.aggregates.tenant.tenant_email_verifier.uuid4")
def test_verifier_key_is_constructed_from_verifier_id_and_uuid_hex_str(mock_uuid4):
    mock_uuid = uuid4()
    mock_uuid4.return_value = mock_uuid

    registrar = TenantEmailVerifier()
    registrar.create(tenant_id=uuid4())

    assert registrar.verification_key is not None
    assert registrar.verification_key == f"{registrar.id}.{mock_uuid.hex}"


@patch("bookt_domain.model.aggregates.tenant.tenant_email_verifier.uuid4")
def test_verify_email_is_success(mock_uuid4):
    mock_uuid = uuid4()
    mock_uuid4.return_value = mock_uuid

    registrar = TenantEmailVerifier()
    registrar.create(tenant_id=uuid4())

    expected_verification_key = f"{registrar.id}.{mock_uuid.hex}"

    registrar.verify_email(
        verification_key=expected_verification_key,
    )

    assert registrar.is_verified


def test_verify_email_errs_on_incorrect_verification_key():
    registrar = TenantEmailVerifier()
    registrar.create(tenant_id=uuid4())

    with pytest.raises(TenantEmailVerificationKeyWasIncorrect):
        registrar.verify_email(verification_key="WRONG KEY")

    assert not registrar.is_verified
