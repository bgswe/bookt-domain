from uuid import UUID, uuid4

from cosmos.domain import AggregateRoot, DomainEvent


class TenantEmailValidator(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, TenantEmailValidatorWasCreated):
            self._apply_validator_created(event=event)
        elif isinstance(event, TenantEmailWasValidated):
            self._apply_email_was_validated(event=event)

    def create(self, tenant_id: UUID):
        self.mutate(
            TenantEmailValidatorWasCreated(
                stream_id=uuid4(),
                tenant_id=tenant_id,
            )
        )

    def _apply_validator_created(self, event: "TenantEmailValidatorWasCreated"):
        self._initialize(
            id=event.stream_id,
            tenant_id=event.tenant_id,
            is_validated=False,
            # TODO: provide better key format, must include validator id
            validation_key=f"{event.stream_id}.{uuid4().hex}",
        )

    def validate_email(self, validation_key: str):
        if validation_key != self.validation_key:
            # TODO: raise not matching exception
            pass

        self.mutate(
            TenantEmailWasValidated(
                tenant_id=self.tenant_id,
            )
        )

    def _apply_email_was_validated(self, event: "TenantEmailWasValidated"):
        self.is_validated = True


class TenantEmailValidatorWasCreated(DomainEvent):
    tenant_id: UUID


class TenantEmailWasValidated(DomainEvent):
    tenant_id: UUID
