from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from cosmos.domain import AggregateRoot, DomainEvent


class TenantRegistration(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, TenantRegistrationInitiated):
            self._apply_registration(event=event)

    def initiate_registration(
        self,
        *,
        stream_id: UUID | None = None,
        tenant_id: UUID | None = None,
        tenant_name: str,
        tenant_registration_email: str,
    ):
        """Entry point into Tenant creation"""

        self.mutate(
            event=TenantRegistrationInitiated(
                stream_id=stream_id if stream_id is not None else uuid4(),
                tenant_id=tenant_id if tenant_id is not None else uuid4(),
                tenant_name=tenant_name,
                tenant_registration_email=tenant_registration_email,
                registered_at=datetime.now(UTC),
            )
        )

    def _apply_registration_initiated(
        self,
        event: TenantRegistrationInitiated,
    ):
        """Initialize a new instance of the Tenant aggregate root"""

        self._initialize(
            stream_id=event.stream_id,
            tenant_id=event.tenant_id,
            tenant_name=event.tenant_name,
            registration_email=event.tenant_registration_email,
            registered_at=event.registered_at,
        )


class TenantRegistrationInitiated(DomainEvent):
    tenant_id: UUID
    tenant_name: str
    tenant_registration_email: str
    initiated_at: datetime


class TenantRegistrationComplete(DomainEvent):
    tenant_id: str