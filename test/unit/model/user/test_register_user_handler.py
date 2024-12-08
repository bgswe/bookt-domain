# from unittest.mock import AsyncMock, MagicMock
# from uuid import uuid4

# import pytest

# from bookt_domain.model.command_handlers import handle_register_user
# from bookt_domain.model.commands import RegisterUser
# from bookt_domain.model.user_registrar import UserRegistrar

# pytest_plugins = ("pytest_asyncio",)


# @pytest.mark.asyncio
# async def test_register_user_handler():
#     uow = MagicMock()
#     uow.repository = MagicMock()
#     uow.repository.get = AsyncMock()
#     uow.repository.save = AsyncMock()

#     mock_registrar = UserRegistrar()
#     mock_registrar.create(tenant_id=uuid4())
#     uow.repository.get.return_value = mock_registrar

#     await handle_register_user(
#         unit_of_work=uow,
#         command=RegisterUser(
#             user_registrar_id=mock_registrar.stream_id,
#             email="some_email",
#             password="some_password",
#         ),
#     )

#     uow.repository.get.assert_called_once_with(id=mock_registrar.stream_id)
#     uow.repository.save.assert_called_once_with(aggregate=mock_registrar)
