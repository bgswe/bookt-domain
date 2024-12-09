from unittest.mock import patch
from uuid import uuid4

import pytest

from bookt_domain.model.tenant_email_validator import (
    TenantEmailValidator,
    TenantValidationKeyWasIncorrect,
)


def test_validator_create_is_success():
    mock_tenant_id = uuid4()

    registrar = TenantEmailValidator()
    registrar.create(tenant_id=mock_tenant_id)

    assert registrar.tenant_id == mock_tenant_id


def test_validator_is_not_validated_after_creation():
    registrar = TenantEmailValidator()
    registrar.create(tenant_id=uuid4())

    assert not registrar.is_validated


@patch("bookt_domain.model.tenant_email_validator.uuid4")
def test_validator_key_is_constructed_from_validator_id_and_uuid_hex_str(mock_uuid4):
    mock_uuid = uuid4()
    mock_uuid4.return_value = mock_uuid

    registrar = TenantEmailValidator()
    registrar.create(tenant_id=uuid4())

    assert registrar.validation_key is not None
    assert registrar.validation_key == f"{registrar.id}.{mock_uuid.hex}"


@patch("bookt_domain.model.tenant_email_validator.uuid4")
def test_validate_email_is_success(mock_uuid4):
    mock_uuid = uuid4()
    mock_uuid4.return_value = mock_uuid

    registrar = TenantEmailValidator()
    registrar.create(tenant_id=uuid4())

    expected_validation_key = f"{registrar.id}.{mock_uuid.hex}"

    registrar.validate_email(
        validation_key=expected_validation_key,
    )

    assert registrar.is_validated


def test_validate_email_errs_on_incorrect_validation_key():
    registrar = TenantEmailValidator()
    registrar.create(tenant_id=uuid4())

    with pytest.raises(TenantValidationKeyWasIncorrect):
        registrar.validate_email(validation_key="WRONG KEY")

    assert not registrar.is_validated
