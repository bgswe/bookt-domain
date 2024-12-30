from __future__ import annotations

from uuid import UUID, uuid4

from cosmos.domain import AggregateRoot, DomainEvent


class TenantRegistrar(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, TenantRegistrarWasCreated):
            self._apply_create(event=event)
        if isinstance(event, TenantWasRegistered):
            self._apply_tenant_registered(event=event)

    def create(self, tenant_registrar_id: UUID):
        self.mutate(
            TenantRegistrarWasCreated(
                stream_id=tenant_registrar_id,
            )
        )

    def _apply_create(self, event: TenantRegistrarWasCreated):
        self._initialize(
            id=event.stream_id,
            registered_tenant_ids=set(),
        )

    def register_tenant(
        self,
        *,
        tenant_id: UUID | None = None,
        tenant_name: str,
        tenant_email: str,
    ):
        """Attempt to register a new tenant into the system."""

        if tenant_id is not None and tenant_id in self.registered_tenant_ids:
            # TODO: raise exception for duplicate ID
            pass

        self.mutate(
            TenantWasRegistered(
                stream_id=self.id,
                tenant_id=tenant_id if tenant_id is not None else uuid4(),
                tenant_name=tenant_name,
                tenant_email=tenant_email,
            )
        )

    def _apply_tenant_registered(
        self,
        event: TenantWasRegistered,
    ):
        """Initialize a new instance of the Tenant aggregate root"""

        self.registered_tenant_ids.add(event.tenant_id)


class TenantRegistrarWasCreated(DomainEvent):
    ...


class TenantWasRegistered(DomainEvent):
    tenant_id: UUID
    tenant_name: str
    tenant_email: str
