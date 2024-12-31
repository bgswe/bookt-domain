from uuid import UUID, uuid4

from cosmos.domain import AggregateRoot, DomainEvent


class TenantEmailVerifierWasCreated(DomainEvent):
    tenant_id: UUID
    verification_key: str


class TenantEmailWasVerified(DomainEvent):
    tenant_id: UUID


class TenantEmailVerificationKeyWasIncorrect(Exception):
    ...


class TenantEmailVerifier(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, TenantEmailVerifierWasCreated):
            self._apply_verifier_created(event=event)
        elif isinstance(event, TenantEmailWasVerified):
            self._apply_email_was_verified(event=event)

    def create(self, tenant_id: UUID):
        stream_id = uuid4()

        self.mutate(
            TenantEmailVerifierWasCreated(
                stream_id=stream_id,
                tenant_id=tenant_id,
                verification_key=f"{stream_id}.{uuid4().hex}",
            )
        )

    def _apply_verifier_created(self, event: TenantEmailVerifierWasCreated):
        self._initialize(
            id=event.stream_id,
            tenant_id=event.tenant_id,
            verification_key=event.verification_key,
            is_verified=False,
        )

    def verify_email(self, verification_key: str):
        if verification_key != self.verification_key:
            raise TenantEmailVerificationKeyWasIncorrect

        self.mutate(
            TenantEmailWasVerified(
                stream_id=self.id,
                tenant_id=self.tenant_id,
            )
        )

    def _apply_email_was_verified(self, event: TenantEmailWasVerified):
        self.is_verified = True
