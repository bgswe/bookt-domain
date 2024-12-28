from uuid import UUID, uuid4

from cosmos.domain import AggregateRoot, DomainEvent


class UserEmailValidatorWasCreated(DomainEvent):
    user_id: UUID
    validator_key: str


class UserEmailValidator(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, UserEmailValidatorWasCreated):
            self._apply_validator_created(event=event)

    def create(self, user_id: UUID):
        stream_id = uuid4()

        self.mutate(
            UserEmailValidatorWasCreated(
                stream_id=stream_id,
                user_id=user_id,
                validator_key=f"{stream_id}.{uuid4().hex}",
            )
        )

    def _apply_validator_created(self, event: UserEmailValidatorWasCreated):
        self._initialize(
            id=event.stream_id,
            user_id=event.user_id,
            validation_key=event.validator_key,
            is_validated=False,
        )
