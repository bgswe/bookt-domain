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


class UserRegistrarWasCreated(DomainEvent):
    ...


class EligibleTenantIDAddedToUserRegistrar(DomainEvent):
    tenant_id: UUID


class UserWasRegistered(DomainEvent):
    user_id: UUID
    tenant_id: UUID
    email: str
    roles: List[UserRoles]


class TenantIDIsNotEligibleForUserRegistration(Exception):
    ...


class UserIDHasAlreadyBeenRegistered(Exception):
    ...


class UserEmailHasAlreadyBeenRegistered(Exception):
    ...


class UserRegistrar(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, UserRegistrarWasCreated):
            self._apply_create(event=event)
        elif isinstance(event, UserWasRegistered):
            self._apply_register_user(event=event)
        elif isinstance(event, EligibleTenantIDAddedToUserRegistrar):
            self._apply_add_eligible_tenant_id(event=event)

    def create(self, user_registrar_id: UUID):
        self.mutate(
            event=UserRegistrarWasCreated(
                stream_id=user_registrar_id,
            )
        )

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
        tenant_id: UUID,
        user_id: UUID | None = None,
        email: str,
        roles: List[UserRoles],
    ):
        """Entry point into User creation"""

        if user_id is not None and user_id in self.created_user_ids:
            raise UserIDHasAlreadyBeenRegistered

        if email in self.created_user_emails:
            raise UserEmailHasAlreadyBeenRegistered

        if tenant_id not in self.eligible_tenant_ids:
            raise TenantIDIsNotEligibleForUserRegistration

        self.mutate(
            event=UserWasRegistered(
                stream_id=self.id,
                tenant_id=tenant_id,
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

    def add_eligible_tenant_id(self, tenant_id: UUID):
        self.mutate(
            EligibleTenantIDAddedToUserRegistrar(
                stream_id=self.id,
                tenant_id=tenant_id,
            )
        )

    def _apply_add_eligible_tenant_id(
        self, event: EligibleTenantIDAddedToUserRegistrar
    ):
        self.eligible_tenant_ids.add(event.tenant_id)
