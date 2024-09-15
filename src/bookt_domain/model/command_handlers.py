from cosmos import UnitOfWork

from bookt_domain.model.commands import RegisterTenant, RegisterUser
from bookt_domain.model.tenant_registration import TenantRegistration
from bookt_domain.model.user_registration import UserRegistration


async def handle_tenant_registration(
    unit_of_work: UnitOfWork,
    command: RegisterTenant,
):
    """Initiates the registration process for a Tenant"""

    registration = TenantRegistration()

    registration.initiate_registration(
        stream_id=command.tenant_registration_id,
        tenant_id=command.tenant_id,
        tenant_name=command.tenant_name,
        tenant_registration_email=command.tenant_registration_email,
    )

    await unit_of_work.repository.save(registration)


async def handle_user_registration(
    unit_of_work: UnitOfWork,
    command: RegisterUser,
):
    """Initiates the registration process for a User"""

    registration = UserRegistration()

    registration.initiate_registration(
        id=command.user_id,
        tenant_id=command.tenant_id,
        email=command.email,
        password=command.password,
        first_name=command.first_name,
        last_name=command.last_name,
    )

    await unit_of_work.repository.save(registration)


COMMAND_HANDLERS = {
    "RegisterTenant": handle_tenant_registration,
    "RegisterUser": handle_user_registration,
}
