from cosmos import UnitOfWork

from bookt_domain.model.commands import RegisterTenant, RegisterUser
from bookt_domain.model.tenant import Tenant
from bookt_domain.model.user import User


async def handle_tenant_registration(
    unit_of_work: UnitOfWork,
    command: RegisterTenant,
):
    """Initiates the registration process for a Tenant"""

    tenant = Tenant()

    tenant.register(
        id=command.tenant_id,
        tenant_name=command.tenant_name,
    )

    await unit_of_work.repository.save(tenant)


async def handle_user_registration(
    unit_of_work: UnitOfWork,
    command: RegisterUser,
):
    """Initiates the registration process for a User"""

    user = User()

    user.create(
        id=command.user_id,
        tenant_id=command.tenant_id,
        email=command.email,
        password=command.password,
        first_name=command.first_name,
        last_name=command.last_name,
    )

    await unit_of_work.repository.save(user)


COMMAND_HANDLERS = {
    "RegisterTenant": handle_tenant_registration,
    "RegisterUser": handle_user_registration,
}
