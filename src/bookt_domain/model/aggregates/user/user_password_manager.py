from uuid import UUID, uuid4

from cosmos.domain import AggregateRoot, DomainEvent


class UserPasswordManagerWasCreated(DomainEvent):
    user_id: UUID
    initial_password_key: str


class UserPasswordWasUpdated(DomainEvent):
    user_id: UUID
    new_hashed_password: str


class SetPasswordKeyWasInvalid(Exception):
    ...


class UserPasswordManager(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, UserPasswordManagerWasCreated):
            self._apply_created(event=event)

    def _apply_created(self, event: UserPasswordManagerWasCreated):
        self._initialize(
            id=event.stream_id,
            user_id=event.user_id,
            initial_password_key=event.initial_password_key,
            hashed_password=None,
        )

    def create(self, user_id: UUID):
        stream_id = uuid4()

        self.mutate(
            event=UserPasswordManagerWasCreated(
                stream_id=stream_id,
                user_id=user_id,
                initial_password_key=f"{stream_id}.{uuid4().hex}",
            )
        )

    def set_password(self, key: str, password: str):
        if self.hashed_password is None and key != self.initial_password_key:
            raise SetPasswordKeyWasInvalid

        # NOTE: Reject change if not None, and key doesn't match current reset key

        # NOTE: Need to adjudicate and hash password here

        self.mutate(
            event=UserPasswordWasUpdated(
                stream_id=self.id,
                user_id=self.user_id,
                new_hashed_password=f"HASHED VERSION OF {password}",
            )
        )
