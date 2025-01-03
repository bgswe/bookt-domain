from datetime import datetime as dt
from datetime import timezone
from uuid import UUID, uuid4

from cosmos.domain import AggregateRoot, DomainEvent


class UserAuthenticatorWasCreated(DomainEvent):
    user_id: UUID


class UserWasAuthenticated(DomainEvent):
    user_id: UUID
    timestamp: dt


class UserAuthenticatorCurrentPasswordHashWasUpdated(DomainEvent):
    current_password_hash: str


class IncorrectPasswordProvided(Exception):
    ...


class AuthenticationAttemptWithNoSetPassword(Exception):
    ...


class UserAuthenticator(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, UserAuthenticatorWasCreated):
            self._apply_authenticator_was_created(event=event)
        elif isinstance(event, UserWasAuthenticated):
            self._apply_user_was_authenticated(event=event)
        elif isinstance(event, UserAuthenticatorCurrentPasswordHashWasUpdated):
            self._apply_current_password_hash_was_updated(event=event)

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
            password_hash=None,
            last_authentication=None,
            authentication_count=0,
        )

    def authenticate(self, password: str):
        # cannot allow authentication before a password hash is set
        if self.password_hash is None:
            raise AuthenticationAttemptWithNoSetPassword

        # compare provided password to stored hash w/ bcrypt
        if self.password_hash != password:  # not right, very bad, change
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

    def update_current_password_hash(self, password_hash: str):
        self.mutate(
            event=UserAuthenticatorCurrentPasswordHashWasUpdated(
                stream_id=self.id,
                current_password_hash=password_hash,
            )
        )

    def _apply_current_password_hash_was_updated(
        self, event: UserAuthenticatorCurrentPasswordHashWasUpdated
    ):
        self.password_hash = event.current_password_hash
