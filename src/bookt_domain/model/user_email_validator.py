from uuid import UUID, uuid4

from cosmos.domain import AggregateRoot, DomainEvent


class UserEmailValidatorWasCreated(DomainEvent):
    user_id: UUID
    validator_key: str


class UserEmailWasValidated(DomainEvent):
    user_id: UUID


class UserEmailValidationKeyWasIncorrect(Exception):
    ...


class UserEmailValidator(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, UserEmailValidatorWasCreated):
            self._apply_validator_created(event=event)
        elif isinstance(event, UserEmailWasValidated):
            self._apply_email_was_validated(event=event)

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

    def validate_email(self, validation_key: str):
        if validation_key != self.validation_key:
            raise UserEmailValidationKeyWasIncorrect

        self.mutate(
            UserEmailWasValidated(
                stream_id=self.id,
                user_id=self.user_id,
            )
        )

    def _apply_email_was_validated(self, event: UserEmailWasValidated):
        self.is_validated = True
