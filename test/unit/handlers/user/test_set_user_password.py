from unittest.mock import MagicMock

import pytest

from bookt_domain.model.command_handlers import handle_set_user_password
from bookt_domain.model.commands import SetUserPassword


@pytest.mark.asyncio
async def test_set_user_password_correctly_gets_manager_id_from_key(mock_uow):
    mock_manager_id = "MOCK_MANAGER_ID"
    mock_random_key = "MOCK_RANDOM_KEY"

    mock_command = SetUserPassword(
        set_password_key=f"{mock_manager_id}.{mock_random_key}",
        password="MOCK PASSWORD",
    )

    await handle_set_user_password(
        unit_of_work=mock_uow,
        command=mock_command,
    )

    mock_uow.repository.get.assert_called_once_with(
        id=mock_manager_id,
        aggregate_root_class=UserPasswordManager,
    )


@pytest.mark.asyncio
async def test_user_password_manager_correctly_gets_random_key_from_set_password_key(
    make_mock_uow,
):
    mock_manager = MagicMock()
    mock_uow = make_mock_uow(get_return_value=mock_manager)

    mock_manager_id = "MOCK_MANAGER_ID"
    mock_random_key = "MOCK_RANDOM_KEY"
    mock_password = "MOCK_PASSWORD"

    mock_command = SetUserPassword(
        set_password_key=f"{mock_manager_id}.{mock_random_key}",
        password=mock_password,
    )

    await handle_set_user_password(
        unit_of_work=mock_uow,
        command=mock_command,
    )

    mock_manager.set_password.assert_called_once_with(
        key=f"{mock_manager_id}.{mock_random_key}",
        password=mock_password,
    )
