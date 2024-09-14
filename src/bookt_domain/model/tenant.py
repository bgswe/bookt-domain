from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from cosmos.domain import AggregateRoot, DomainEvent


class Tenant(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, TenantRegistered):
            self._apply_registration(event=event)

    def register(self, *, id: UUID | None = None, name: str):
        """Entry point into Tenant creation"""

        self.mutate(
            event=TenantRegistered(
                stream_id=id if id is not None else uuid4(),
                tenant_name=name,
                registered_at=datetime.now(UTC),
            )
        )

    def _apply_registration(self, event: TenantRegistered):
        """Initialize a new instance of the Tenant aggregate root"""

        self._initialize(
            id=event.stream_id,
            name=event.name,
            registered_at=event.registered_at,
        )


class TenantRegistered(DomainEvent):
    tenant_name: str
    registered_at: datetime
