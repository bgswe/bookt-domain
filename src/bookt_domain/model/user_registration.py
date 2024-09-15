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


class UserRegistration(AggregateRoot):
    def initiate_registration(
        self,
        *,
        stream_id: UUID | None = None,
        user_id: UUID | None = None,
        tenant_id: UUID,
        email: str,
        roles: List[UserRoles],
    ):
        """Entry point into User creation"""

        self.mutate(
            event=UserRegistrationInitiated(
                stream_id=stream_id if stream_id is not None else uuid4(),
                user_id=user_id if user_id is not None else uuid4(),
                tenant_id=tenant_id,
                email=email,
                roles=roles,
            )
        )

    def _mutate(self, event: DomainEvent):
        if isinstance(event, UserRegistrationInitiated):
            self._apply_registration_initiated(event=event)

    def _apply_registration_initiated(self, event: UserRegistrationInitiated):
        """Initialize a new instance of the User aggregate root"""

        random_password = "password"
        hashed_password = bcrypt.hashpw(
            random_password.encode("utf-8"), bcrypt.gensalt(10)
        )
        hashed_password = hashed_password.decode("utf-8")

        self._initialize(
            stream_id=event.stream_id,
            user_id=event.user_id,
            tenant_id=event.tenant_id,
            email=event.email,
            hashed_password=hashed_password,
            last_login=None,
        )


class UserRegistrationInitiated(DomainEvent):
    stream_id: UUID
    user_id: UUID
    tenant_id: UUID
    email: str
    roles: List[UserRoles]
