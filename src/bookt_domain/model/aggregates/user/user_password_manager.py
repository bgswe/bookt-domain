from uuid import UUID, uuid4

from cosmos.domain import AggregateRoot, DomainEvent


class UserPasswordManagerWasCreated(DomainEvent):
    user_id: UUID


class UserPasswordManager(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, UserPasswordManagerWasCreated):
            self._apply_created(event=event)

    def _apply_created(self, event: UserPasswordManagerWasCreated):
        self._initialize(
            id=event.stream_id,
            user_id=event.user_id,
            hashed_password=None,
        )

    def create(self, user_id: UUID):
        self.mutate(
            event=UserPasswordManagerWasCreated(
                stream_id=uuid4(),
                user_id=user_id,
            )
        )
