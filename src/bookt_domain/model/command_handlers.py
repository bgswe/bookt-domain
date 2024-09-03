from cosmos import UnitOfWork

from bookt_domain.model import Account
from bookt_domain.model.commands import Register


async def handle_registration(
    unit_of_work: UnitOfWork,
    command: Register,
):
    """Initiates the registration process by creating an Account"""

    account = Account()

    account.create(
        id=command.account_id,
        originator_email=command.originator_email,
    )

    await unit_of_work.repository.save(account)


COMMAND_HANDLERS = {
    "Register": handle_registration,
}
