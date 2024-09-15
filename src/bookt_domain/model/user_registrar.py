from __future__ import annotations

from enum import StrEnum, auto
from typing import List
from uuid import UUID, uuid4

# import bcrypt
from cosmos.domain import AggregateRoot, DomainEvent


class UserRoles(StrEnum):
    APP_ADMIN = auto()
    TENANT_ADMIN = auto()
    TENANT_USER = auto()


class UserRegistrar(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, UserRegistrarCreated):
            self._apply_create(event=event)
        if isinstance(event, UserRegistrationInitiated):
            self._apply_registration_initiated(event=event)

    def create(self, tenant_id: UUID):
        self.mutate(event=UserRegistrarCreated(tenant_id=tenant_id))

    def _apply_create(self, event: UserRegistrarCreated):
        self._initialize(tenant_id=event.tenant_id)
        self._created_user_ids = set()

    def initiate_registration(
        self,
        *,
        user_id: UUID | None = None,
        email: str,
        roles: List[UserRoles],
    ):
        """Entry point into User creation"""

        self.mutate(
            event=UserRegistrationInitiated(
                user_id=user_id if user_id is not None else uuid4(),
                tenant_id=self.tenant_id,
                email=email,
                roles=roles,
            )
        )

    def _apply_registration_initiated(self, event: UserRegistrationInitiated):
        self._created_user_ids.add(event.user_id)

        # random_password = "password"
        # hashed_password = bcrypt.hashpw(
        #     random_password.encode("utf-8"), bcrypt.gensalt(10)
        # )
        # hashed_password = hashed_password.decode("utf-8")


class UserRegistrarCreated(DomainEvent):
    tenant_id: UUID


class UserRegistrationInitiated(DomainEvent):
    user_id: UUID
    tenant_id: UUID
    email: str
    roles: List[UserRoles]


class UserRegistrationCompleted(DomainEvent):
    pass
