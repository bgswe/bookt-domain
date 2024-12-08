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
        if isinstance(event, UserRegistrarWasCreated):
            self._apply_create(event=event)
        if isinstance(event, UserWasRegistered):
            self._

    def create(self, user_registrar_id: UUID):
        self.mutate(
            event=UserRegistrarWasCreated(
                stream_id=user_registrar_id,
            )
        )
        return self

    def _apply_create(self, event: UserRegistrarWasCreated):
        self._initialize(
            id=event.stream_id,
            eligible_tenant_ids=set(),
            created_user_ids=set(),
            created_user_emails=set(),
        )

    def register_user(
        self,
        *,
        user_id: UUID | None = None,
        email: str,
        roles: List[UserRoles],
    ):
        """Entry point into User creation"""

        if user_id is not None and self.created_user_ids.has(user_id):
            # TODO: raise exception for user id already being created
            raise Exception("user id has already been used")

        if self.created_user_emails.has(email):
            # TODO: raise exception for user email already being used
            raise Exception("user email has already been used")

        self.mutate(
            event=UserWasRegistered(
                stream_id=self.id,
                tenant_id=self.tenant_id,
                user_id=user_id if user_id is not None else uuid4(),
                email=email,
                roles=roles,
            )
        )

    def _apply_register_user(self, event: UserWasRegistered):
        self.created_user_ids.add(event.user_id)
        self.created_user_emails.add(event.email)

        # random_password = "password"
        # hashed_password = bcrypt.hashpw(
        #     random_password.encode("utf-8"), bcrypt.gensalt(10)
        # )
        # hashed_password = hashed_password.decode("utf-8")


class UserRegistrarWasCreated(DomainEvent):
    ...


class UserWasRegistered(DomainEvent):
    user_id: UUID
    tenant_id: UUID
    email: str
    roles: List[UserRoles]
