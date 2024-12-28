import structlog
from cosmos import UnitOfWork

from bookt_domain.model.commands import (
    RegisterTenant,
    RegisterUser,
    ValidateTenantEmail,
    ValidateUserEmail,
)
from bookt_domain.model.tenant_email_validator import TenantEmailValidator
from bookt_domain.model.tenant_registrar import TenantRegistrar
from bookt_domain.model.user_email_validator import UserEmailValidator
from bookt_domain.model.user_registrar import UserRegistrar, UserRoles

logger = structlog.get_logger()


async def handle_tenant_registration(
    unit_of_work: UnitOfWork,
    command: RegisterTenant,
):
    """Initiates the registration process for a Tenant"""

    registrar = await unit_of_work.repository.get_singleton(
        aggregate_root_class=TenantRegistrar
    )

    registrar.register_tenant(
        tenant_id=command.tenant_id,
        tenant_name=command.tenant_name,
        tenant_email=command.tenant_registration_email,
    )

    await unit_of_work.repository.save(aggregate=registrar)


async def handle_validate_tenant_email(
    unit_of_work: UnitOfWork,
    command: ValidateTenantEmail,
):
    """Confirm the validation of the tenant's registration email"""

    # extract id from validation key
    validator_id = command.validation_key.split(".")[0]

    validator = await unit_of_work.repository.get(
        id=validator_id,
        aggregate_root_class=TenantEmailValidator,
    )

    validator.validate_email(validation_key=command.validation_key)

    await unit_of_work.repository.save(validator)


async def handle_register_user(
    unit_of_work: UnitOfWork,
    command: RegisterUser,
):
    """Initiates the registration process for a User"""

    user_registrar = await unit_of_work.repository.get_singleton(
        aggregate_root_class=UserRegistrar,
    )

    user_registrar.register_user(
        tenant_id=command.tenant_id,
        user_id=command.user_id,
        email=command.email,
        roles=[UserRoles.TENANT_USER],  # TODO: Implement the ability to specify
    )

    await unit_of_work.repository.save(aggregate=user_registrar)


async def handle_validate_user_email(
    unit_of_work: UnitOfWork,
    command: ValidateUserEmail,
):
    """Confirm the validation of the user's email"""

    # extract id from validation key
    validator_id = command.validation_key.split(".")[0]

    validator = await unit_of_work.repository.get(
        id=validator_id,
        aggregate_root_class=UserEmailValidator,
    )

    validator.validate_email(validation_key=command.validation_key)

    await unit_of_work.repository.save(validator)


COMMAND_HANDLERS = {
    "RegisterTenant": handle_tenant_registration,
    "ValidateTenantEmail": handle_validate_tenant_email,
    "RegisterUser": handle_register_user,
}
