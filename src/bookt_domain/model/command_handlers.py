from cosmos import UnitOfWork

from bookt_domain.model.commands import RegisterTenant
from bookt_domain.model.tenant import Tenant


async def handle_registration(
    unit_of_work: UnitOfWork,
    command: RegisterTenant,
):
    """Initiates the registration process by creating an Tenant"""

    tenant = Tenant()

    tenant.register(
        id=command.tenant_id,
        name=command.tenant_name,
    )

    await unit_of_work.repository.save(tenant)


COMMAND_HANDLERS = {
    "RegisterTenant": handle_registration,
}
