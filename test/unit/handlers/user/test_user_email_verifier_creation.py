from unittest.mock import patch
from uuid import uuid4

import pytest

from bookt_domain.model.aggregates.user.user_registrar import (
    UserRoles,
    UserWasRegistered,
)
from bookt_domain.model.event_handlers import create_user_email_verifier


@patch("bookt_domain.model.event_handlers.UserEmailVerifier.create")
@pytest.mark.asyncio
async def test_create_user_email_verifier_for_tenant(mock_verifier_create, mock_uow):
    mock_user_id = uuid4()

    mock_event = UserWasRegistered(
        stream_id=uuid4(),
        user_id=mock_user_id,
        tenant_id=uuid4(),
        roles=[UserRoles.TENANT_USER],
        email="Some User Email",
    )

    await create_user_email_verifier(unit_of_work=mock_uow, event=mock_event)

    mock_verifier_create.assert_called_once_with(user_id=mock_user_id)
    mock_uow.repository.save.assert_called_once()
