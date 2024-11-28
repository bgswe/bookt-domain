import structlog
from cosmos import UnitOfWork

from bookt_domain.model.commands import (
    RegisterTenant,
    RegisterUser,
    ValidateTenantEmail,
)
from bookt_domain.model.tenant_registratrar import TenantRegistratrar
from bookt_domain.model.user_registrar import UserRegistrar, UserRoles

logger = structlog.get_logger()


async def handle_tenant_registration(
    unit_of_work: UnitOfWork,
    command: RegisterTenant,
):
    """Initiates the registration process for a Tenant"""

    registration = TenantRegistratrar()

    registration.initiate_registration(
        stream_id=command.tenant_registration_id,
        tenant_id=command.tenant_id,
        tenant_name=command.tenant_name,
        tenant_registration_email=command.tenant_registration_email,
    )

    await unit_of_work.repository.save(registration)


async def handle_validate_tenant_email(
    unit_of_work: UnitOfWork,
    command: ValidateTenantEmail,
):
    """Confirm the validation of the tenant's registration email"""

    registration = await unit_of_work.repository.get(
        id=command.tenant_registration_id,
        aggregate_root_class=TenantRegistratrar,
    )

    registration.validate_registration_email()
    registration.complete_registration()

    await unit_of_work.repository.save(registration)


async def handle_register_user(
    unit_of_work: UnitOfWork,
    command: RegisterUser,
):
    """Initiates the registration process for a User"""

    user_registrar = await unit_of_work.repository.get(
        id=command.user_registrar_id,
        aggregate_root_class=UserRegistrar,
    )

    user_registrar.initiate_registration(
        stream_id=command.user_registration_id,
        user_id=command.user_id,
        email=command.email,
        roles=[UserRoles.TENANT_USER],  # todo: expose this as option? MT
    )

    await unit_of_work.repository.save(aggregate=user_registrar)


COMMAND_HANDLERS = {
    "RegisterTenant": handle_tenant_registration,
    "ValidateTenantEmail": handle_validate_tenant_email,
    "RegisterUser": handle_register_user,
}
