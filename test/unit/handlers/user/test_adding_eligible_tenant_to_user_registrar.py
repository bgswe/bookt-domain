from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from bookt_domain.model.event_handlers import add_eligible_tenant_to_user_registrar
from bookt_domain.model.tenant_email_validator import TenantEmailWasValidated
from bookt_domain.model.user_registrar import UserRegistrar


@patch("bookt_domain.model.event_handlers.TenantEmailValidator.create")
@pytest.mark.asyncio
async def test_add_eligible_tenant_to_user_registrar_is_success(
    mock_validator_create, make_mock_uow
):
    mock_validator_id = uuid4()
    mock_tenant_id = uuid4()

    mock_event = TenantEmailWasValidated(
        stream_id=mock_validator_id,
        tenant_id=mock_tenant_id,
    )

    mock_user_registrar = MagicMock()
    mock_uow = make_mock_uow(get_singleton_return_value=mock_user_registrar)

    await add_eligible_tenant_to_user_registrar(unit_of_work=mock_uow, event=mock_event)

    mock_uow.repository.get_singleton.assert_called_once_with(
        aggregate_root_class=UserRegistrar
    )
    mock_user_registrar.add_eligible_tenant_id.assert_called_once_with(
        tenant_id=mock_tenant_id
    )
    mock_uow.repository.save.assert_called_once_with(aggregate=mock_user_registrar)
