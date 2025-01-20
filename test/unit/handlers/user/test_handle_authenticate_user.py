from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from bookt_domain.model.aggregates.user.user_authenticator import UserAuthenticator
from bookt_domain.model.command_handlers import handle_authenticate_user
from bookt_domain.model.commands import AuthenticateUser


@pytest.mark.asyncio
async def test_authenticate_user_is_success(
    make_mock_uow,
):
    mock_uow = make_mock_uow()
    mock_authenticator = MagicMock()
    mock_uow.repository.get.return_value = mock_authenticator

    mock_password = "asdfasdfas"
    mock_authenticator_id = uuid4()

    command = AuthenticateUser(
        user_authenticator_id=mock_authenticator_id,
        password=mock_password,
    )

    await handle_authenticate_user(unit_of_work=mock_uow, command=command)

    mock_uow.repository.get.assert_called_once_with(
        id=mock_authenticator_id,
        aggregate_root_class=UserAuthenticator,
    )

    mock_authenticator.authenticate.assert_called_once_with(
        password=mock_password,
    )

    mock_uow.repository.save.assert_called_once_with(
        aggregate=mock_authenticator,
    )
