from unittest.mock import patch
from uuid import uuid4

import pytest

from bookt_domain.model.event_handlers import create_user_email_validator
from bookt_domain.model.user_registrar import UserRoles, UserWasRegistered


@patch("bookt_domain.model.event_handlers.UserEmailValidator.create")
@pytest.mark.asyncio
async def test_create_user_email_validator_for_tenant(mock_validator_create, mock_uow):
    mock_user_id = uuid4()

    mock_event = UserWasRegistered(
        stream_id=uuid4(),
        user_id=mock_user_id,
        tenant_id=uuid4(),
        roles=[UserRoles.TENANT_USER],
        email="Some User Email",
    )

    await create_user_email_validator(unit_of_work=mock_uow, event=mock_event)

    mock_validator_create.assert_called_once_with(user_id=mock_user_id)
    mock_uow.repository.save.assert_called_once()
