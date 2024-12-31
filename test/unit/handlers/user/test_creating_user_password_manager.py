from unittest.mock import patch
from uuid import uuid4

import pytest

from bookt_domain.model.aggregates.user.user_email_verifier import UserEmailWasVerified
from bookt_domain.model.event_handlers import create_user_password_manager


@patch("bookt_domain.model.event_handlers.UserPasswordManager.create")
@pytest.mark.asyncio
async def test_create_user_password_manager_is_success(
    mock_manager_create, make_mock_uow
):
    mock_user_id = uuid4()

    mock_event = UserEmailWasVerified(
        stream_id=uuid4(),
        user_id=mock_user_id,
    )

    mock_uow = make_mock_uow()
    await create_user_password_manager(unit_of_work=mock_uow, event=mock_event)

    mock_manager_create.assert_called_once_with(
        user_id=mock_event.user_id,
    )
    mock_uow.repository.save.assert_called_once()
