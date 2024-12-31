from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from bookt_domain.model.aggregates.tenant.tenant_email_verifier import (
    TenantEmailWasVerified,
)
from bookt_domain.model.aggregates.user.user_registrar import UserRegistrar
from bookt_domain.model.event_handlers import add_eligible_tenant_to_user_registrar


@pytest.mark.asyncio
async def test_add_eligible_tenant_to_user_registrar_is_success(make_mock_uow):
    mock_verifier_id = uuid4()
    mock_tenant_id = uuid4()

    mock_event = TenantEmailWasVerified(
        stream_id=mock_verifier_id,
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
