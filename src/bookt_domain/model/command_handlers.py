import structlog
from cosmos import UnitOfWork

from bookt_domain.model.commands import (  # RegisterUser,
    RegisterTenant,
    ValidateTenantEmail,
)
from bookt_domain.model.tenant_registration import TenantRegistration

# from bookt_domain.model.user_registrar import UserRegistrar


logger = structlog.get_logger()


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


async def handle_validate_tenant_email(
    unit_of_work: UnitOfWork,
    command: ValidateTenantEmail,
):
    """Confirm the validation of the tenant's registration email"""

    registration = await unit_of_work.repository.get(
        id=command.tenant_registration_id,
        aggregate_root_class=TenantRegistration,
    )

    registration.validate_registration_email()
    registration.complete_registration()

    log = logger.bind(events=registration.events)
    log.bind(m_id_0=registration.events[0].id)
    log.bind(m_id_1=registration.events[1].id)
    log.info("FROM HANDLE TENANT EMAIL")

    await unit_of_work.repository.save(registration)


# async def handle_user_registration(
#     unit_of_work: UnitOfWork,
#     command: RegisterUser,
# ):
#     """Initiates the registration process for a User"""

#     user_registrar = UserRegistration()

#     registration.initiate_registration(
#         stream_id=command.user_registration_id,
#         user_id=command.user_id,
#         tenant_id=command.tenant_id,
#         email=command.email,
#         password=command.password,
#     )

#     await unit_of_work.repository.save(registration)


COMMAND_HANDLERS = {
    "RegisterTenant": handle_tenant_registration,
    "ValidateTenantEmail": handle_validate_tenant_email,
    # "RegisterUser": handle_user_registration,
}
