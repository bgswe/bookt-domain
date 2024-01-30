from cosmos import UnitOfWork, command
from cosmos.domain import Command

from bookt_domain.model import Account
from bookt_domain.service.commands import Register


@command
async def handle_registration(
    uow: UnitOfWork,
    command: Register,
):
    """Initiates the registration process by creating an Account"""

    account = Account()

    account.create(
        id=command.account_id,
        originator_email=command.originator_email,
    )

    await uow.repository.save(account)


COMMAND_HANDLERS = {
    "Register": handle_registration,
}


async def handle_command(command: Command):
    command_name = command.__class__.__name__

    handler = COMMAND_HANDLERS.get(command_name, [])
    await handler(command=command)
