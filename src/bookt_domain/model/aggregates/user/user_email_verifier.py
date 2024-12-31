from uuid import UUID, uuid4

from cosmos.domain import AggregateRoot, DomainEvent


class UserEmailVerifierWasCreated(DomainEvent):
    user_id: UUID
    verification_key: str


class UserEmailWasVerified(DomainEvent):
    user_id: UUID


class UserEmailVerificationKeyWasIncorrect(Exception):
    ...


class UserEmailVerifier(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, UserEmailVerifierWasCreated):
            self._apply_verifier_created(event=event)
        elif isinstance(event, UserEmailWasVerified):
            self._apply_email_was_verified(event=event)

    def create(self, user_id: UUID):
        stream_id = uuid4()

        self.mutate(
            UserEmailVerifierWasCreated(
                stream_id=stream_id,
                user_id=user_id,
                verification_key=f"{stream_id}.{uuid4().hex}",
            )
        )

    def _apply_verifier_created(self, event: UserEmailVerifierWasCreated):
        self._initialize(
            id=event.stream_id,
            user_id=event.user_id,
            verification_key=event.verification_key,
            is_verified=False,
        )

    def verify_email(self, verification_key: str):
        if verification_key != self.verification_key:
            raise UserEmailVerificationKeyWasIncorrect

        self.mutate(
            UserEmailWasVerified(
                stream_id=self.id,
                user_id=self.user_id,
            )
        )

    def _apply_email_was_verified(self, event: UserEmailWasVerified):
        self.is_verified = True
