from __future__ import annotations

from enum import StrEnum, auto
from typing import List
from uuid import UUID, uuid4

import bcrypt
from cosmos.domain import AggregateRoot, DomainEvent


class UserRoles(StrEnum):
    APP_ADMIN = auto()
    TENANT_ADMIN = auto()
    TENANT_USER = auto()


class User(AggregateRoot):
    def create(
        self,
        *,
        id: UUID = None,
        tenant_id: UUID,
        email: str,
        roles: List[UserRoles],
        first_name: str = None,
        last_name: str = None,
    ):
        """Entry point into User creation"""

        self.mutate(
            event=UserCreated(
                stream_id=id if id is not None else uuid4(),
                tenant_id=tenant_id,
                email=email,
                roles=roles,
                first_name=first_name,
                last_name=last_name,
            )
        )

    def _mutate(self, event: DomainEvent):
        if isinstance(event, UserCreated):
            self._apply_create(event=event)

    def _apply_create(self, event: UserCreated):
        """Initialize a new instance of the User aggregate root"""

        random_password = "password"
        hashed_password = bcrypt.hashpw(
            random_password.encode("utf-8"), bcrypt.gensalt(10)
        )
        hashed_password = hashed_password.decode("utf-8")

        self._initialize(
            id=event.stream_id,
            tenant_id=event.tenant_id,
            email=event.email,
            first_name=event.first_name,
            last_name=event.last_name,
            hashed_password=hashed_password,
            last_login=None,
        )


class UserCreated(DomainEvent):
    stream_id: UUID
    tenant_id: UUID
    email: str
    roles: List[UserRoles]
    first_name: str | None = None
    last_name: str | None = None
