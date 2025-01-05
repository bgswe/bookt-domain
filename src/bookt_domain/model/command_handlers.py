import structlog
from cosmos import UnitOfWork, command

from bookt_domain.model.aggregates.tenant.tenant_email_verifier import (
    TenantEmailVerifier,
)
from bookt_domain.model.aggregates.tenant.tenant_registrar import TenantRegistrar
from bookt_domain.model.aggregates.user.user_email_verifier import UserEmailVerifier
from bookt_domain.model.aggregates.user.user_password_manager import UserPasswordManager
from bookt_domain.model.aggregates.user.user_registrar import UserRegistrar, UserRoles
from bookt_domain.model.commands import (
    RegisterTenant,
    RegisterUser,
    SetUserPassword,
    VerifyTenantEmail,
    VerifyUserEmail,
)

logger = structlog.get_logger()


@command(command_type_name="RegisterTenant")
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


@command(command_type_name="VerifyTenantEmail")
async def handle_verify_tenant_email(
    unit_of_work: UnitOfWork,
    command: VerifyTenantEmail,
):
    """Verify the email provided on tenant registration"""

    # extract id from verification key
    verifier_id = command.verification_key.split(".")[0]

    verifier = await unit_of_work.repository.get(
        id=verifier_id,
        aggregate_root_class=TenantEmailVerifier,
    )

    verifier.verify_email(verification_key=command.verification_key)

    await unit_of_work.repository.save(verifier)


@command(command_type_name="RegisterUser")
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


@command(command_type_name="VerifyUserEmail")
async def handle_verify_user_email(
    unit_of_work: UnitOfWork,
    command: VerifyUserEmail,
):
    """Verify the mail provided by the user"""

    # extract id from verification key
    verifier_id = command.verification_key.split(".")[0]

    verifier = await unit_of_work.repository.get(
        id=verifier_id,
        aggregate_root_class=UserEmailVerifier,
    )

    verifier.verify_email(verification_key=command.verification_key)

    await unit_of_work.repository.save(aggregate=verifier)


@command(command_type_name="SetUserPassword")
async def handle_set_user_password(
    unit_of_work: UnitOfWork,
    command: SetUserPassword,
):
    # extract stream id from set password key
    password_manager_id = command.set_password_key.split(".")[0]

    password_manager = await unit_of_work.repository.get(
        id=password_manager_id,
        aggregate_root_class=UserPasswordManager,
    )

    password_manager.set_password(
        key=command.set_password_key,
        password=command.password,
    )

    await unit_of_work.repository.save(aggregate=password_manager)
