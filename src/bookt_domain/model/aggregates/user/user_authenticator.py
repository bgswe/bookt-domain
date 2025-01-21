from datetime import datetime as dt
from datetime import timezone
from uuid import UUID, uuid4

import bcrypt
from cosmos.domain import AggregateRoot, DomainEvent


class UserAuthenticatorWasCreated(DomainEvent):
    user_id: UUID


class SetUserPasswordKeyWasGenerated(DomainEvent):
    user_id: UUID
    key: str


class UserPasswordWasUpdated(DomainEvent):
    user_id: UUID
    new_hashed_password: str


class UserWasAuthenticated(DomainEvent):
    user_id: UUID
    timestamp: dt


class SetPasswordKeyWasInvalid(Exception):
    ...


class AuthenticationAttemptWithNoSetPassword(Exception):
    ...


class IncorrectPasswordProvided(Exception):
    ...


class UserAuthenticator(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, UserAuthenticatorWasCreated):
            self._apply_authenticator_was_created(event=event)
        elif isinstance(event, SetUserPasswordKeyWasGenerated):
            self._apply_key_was_generated(event=event)
        elif isinstance(event, UserPasswordWasUpdated):
            self._apply_password_was_updated(event=event)
        elif isinstance(event, UserWasAuthenticated):
            self._apply_user_was_authenticated(event=event)

    def create(self, user_id: UUID):
        self.mutate(
            UserAuthenticatorWasCreated(
                stream_id=uuid4(),
                user_id=user_id,
            )
        )

    def _apply_authenticator_was_created(self, event: UserAuthenticatorWasCreated):
        self._initialize(
            id=event.stream_id,
            user_id=event.user_id,
            set_password_key=None,
            password_hash=None,
            last_authentication=None,
            authentication_count=0,
        )

    def generate_set_password_key(self):
        self.mutate(
            event=SetUserPasswordKeyWasGenerated(
                stream_id=self.id,
                user_id=self.user_id,
                key=f"{self.id}.{uuid4().hex}",
            )
        )

    def _apply_key_was_generated(self, event: SetUserPasswordKeyWasGenerated):
        self.set_password_key = event.key

    def update_password(self, key: str, password: str):
        if self.set_password_key is None or key != self.set_password_key:
            raise SetPasswordKeyWasInvalid

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

    def _apply_password_was_updated(self, event: UserPasswordWasUpdated):
        self.set_password_key = None
        self.password_hash = event.new_hashed_password

    def authenticate(self, password: str):
        # cannot allow authentication before a password hash is set
        if self.password_hash is None:
            raise AuthenticationAttemptWithNoSetPassword

        # compare provided password to stored hash w/ bcrypt
        if not bcrypt.checkpw(
            password.encode("utf-8"),
            self.password_hash.encode("utf-8"),
        ):
            raise IncorrectPasswordProvided

        self.mutate(
            UserWasAuthenticated(
                stream_id=self.id,
                user_id=self.user_id,
                timestamp=dt.now(timezone.utc).replace(tzinfo=None),
            )
        )

    def _apply_user_was_authenticated(self, event: UserWasAuthenticated):
        self.authentication_count += 1
        self.last_authentication = event.timestamp
