from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from bookt_domain.model.aggregates.user.user_registrar import UserRegistrar, UserRoles
from bookt_domain.model.command_handlers import handle_register_user
from bookt_domain.model.commands import RegisterUser


@pytest.mark.asyncio
async def test_user_registration_handler_is_success(mock_uow):
    mock_registrar = MagicMock()
    mock_uow.repository.get_singleton.return_value = mock_registrar

    mock_tenant_id = uuid4()
    mock_user_id = uuid4()
    mock_email = "some_email@example.com"

    await handle_register_user(
        unit_of_work=mock_uow,
        command=RegisterUser(
            tenant_id=mock_tenant_id,
            user_id=mock_user_id,
            email=mock_email,
        ),
    )

    mock_uow.repository.get_singleton.assert_called_once_with(
        aggregate_root_class=UserRegistrar
    )
    mock_registrar.register_user.assert_called_once_with(
        tenant_id=mock_tenant_id,
        user_id=mock_user_id,
        email=mock_email,
        roles=[UserRoles.TENANT_USER],
    )
    mock_uow.repository.save.assert_called_once_with(aggregate=mock_registrar)
