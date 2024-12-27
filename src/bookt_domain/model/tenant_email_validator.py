from uuid import UUID, uuid4

from cosmos.domain import AggregateRoot, DomainEvent


class TenantEmailValidatorWasCreated(DomainEvent):
    tenant_id: UUID
    validation_key: str


class TenantEmailWasValidated(DomainEvent):
    tenant_id: UUID


class TenantValidationKeyWasIncorrect(Exception):
    ...


class TenantEmailValidator(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, TenantEmailValidatorWasCreated):
            self._apply_validator_created(event=event)
        elif isinstance(event, TenantEmailWasValidated):
            self._apply_email_was_validated(event=event)

    def create(self, tenant_id: UUID):
        stream_id = uuid4()

        self.mutate(
            TenantEmailValidatorWasCreated(
                stream_id=stream_id,
                tenant_id=tenant_id,
                validation_key=f"{stream_id}.{uuid4().hex}",
            )
        )

    def _apply_validator_created(self, event: TenantEmailValidatorWasCreated):
        self._initialize(
            id=event.stream_id,
            tenant_id=event.tenant_id,
            validation_key=event.validation_key,
            is_validated=False,
        )

    def validate_email(self, validation_key: str):
        if validation_key != self.validation_key:
            raise TenantValidationKeyWasIncorrect

        self.mutate(
            TenantEmailWasValidated(
                stream_id=self.id,
                tenant_id=self.tenant_id,
            )
        )

    def _apply_email_was_validated(self, event: TenantEmailWasValidated):
        self.is_validated = True
