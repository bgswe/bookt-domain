from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from bookt_domain.model.tenant_registrar import TenantRegistrar

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
def make_mock_uow():
    def make(
        get_singleton_return_value: MagicMock | None = None,
        get_return_value: MagicMock | None = None,
    ):
        uow = MagicMock()
        uow.repository = MagicMock()
        uow.repository.get = AsyncMock()
        uow.repository.get_singleton = AsyncMock()
        uow.repository.save = AsyncMock()

        if get_singleton_return_value is None:
            get_singleton_return_value = MagicMock()

        if get_return_value is None:
            get_return_value = MagicMock()

        uow.repository.get_singleton.return_value = get_singleton_return_value
        uow.repository.get.return_value = get_return_value
        return uow

    return make


@pytest.fixture
def mock_uow(make_mock_uow):
    return make_mock_uow()


@pytest.fixture
def mock_tenant_registrar():
    mock_registrar_id = uuid4()
    mock_registrar = TenantRegistrar()
    mock_registrar.create(tenant_registrar_id=mock_registrar_id)
    return mock_registrar
