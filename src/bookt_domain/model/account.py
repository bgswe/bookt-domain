from __future__ import annotations

from uuid import UUID, uuid4

from cosmos.domain import AggregateRoot, DomainEvent


class Account(AggregateRoot):
    def _mutate(self, event: DomainEvent):
        if isinstance(event, AccountCreated):
            self._apply_create(event=event)

    def create(self, *, id: UUID | None = None, originator_email: str):
        """Entry point into account creation"""

        self.mutate(
            event=AccountCreated(
                stream_id=id if id else uuid4(),
                originator_email=originator_email,
            )
        )

    def _apply_create(self, event: AccountCreated):
        """Initialize a new instance of the Account aggregate root"""

        self._initialize(
            id=event.stream_id,
            originator_email=event.originator_email,
        )


class AccountCreated(DomainEvent):
    originator_email: str
