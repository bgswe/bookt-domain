from uuid import UUID, uuid4

import bcrypt
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
        elif isinstance(event, UserPasswordWasUpdated):
            self._apply_password_was_updated(event=event)

    def _apply_created(self, event: UserPasswordManagerWasCreated):
        self._initialize(
            id=event.stream_id,
            user_id=event.user_id,
            initial_password_key=event.initial_password_key,
            password_history=set(),
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

    def _apply_password_was_updated(self, event: UserPasswordWasUpdated):
        self.password_history.add(event.new_hashed_password)
        self.initial_password_key = None

    def set_password(self, key: str, password: str):
        if not self.password_history and key != self.initial_password_key:
            raise SetPasswordKeyWasInvalid

        # NOTE: Reject change if not None, and key doesn't match current reset key
        # if self.password_history and key != self.current_password_key:
        #   raise SetPasswordKeyWasInvalid

        # NOTE: Need to adjudicate password rules here

        password_bytes = password.encode("utf-8")
        password_salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password=password_bytes, salt=password_salt)

        self.mutate(
            event=UserPasswordWasUpdated(
                stream_id=self.id,
                user_id=self.user_id,
                new_hashed_password=password_hash,
            )
        )
