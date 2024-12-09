from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from bookt_domain.model.tenant_registrar import TenantRegistrar

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.repository = MagicMock()
    uow.repository.get_singleton = AsyncMock()
    uow.repository.save = AsyncMock()
    return uow


@pytest.fixture
def mock_tenant_registrar():
    mock_registrar_id = uuid4()
    mock_registrar = TenantRegistrar()
    mock_registrar.create(tenant_registrar_id=mock_registrar_id)
    return mock_registrar
