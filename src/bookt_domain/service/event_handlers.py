from cosmos import UnitOfWork
from cosmos.decorators import Event, event

from bookt_domain.model.account import AccountCreated
from bookt_domain.model.user import User, UserCreated, UserRoles


@event
async def create_originator_user(uow: UnitOfWork, event: AccountCreated):
    """Create a new user for creator of new account"""

    user = User()

    user.create(
        account_id=event.stream_id,
        email=event.originator_email,
        roles=[UserRoles.ACCOUNT_ADMIN],
    )

    await uow.repository.save(aggregate=user)


@event
async def handler_user_create(uow: UnitOfWork, event: UserCreated):
    user = uow.repository.get(id=id, aggregate_root_class=User)

    print(user)


EVENT_HANDLERS = {
    "AccountCreated": [create_originator_user],
    "UserCreated": [],
}


async def handle_event(event: Event):
    event_name = event.__class__.__name__

    handlers = EVENT_HANDLERS.get(event_name, [])
    for handler in handlers:
        await handler(event=event)
