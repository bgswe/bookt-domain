import structlog
from cosmos import UnitOfWork

from bookt_domain.model.aggregates.tenant.tenant_email_verifier import (
    TenantEmailVerifier,
    TenantEmailWasVerified,
)
from bookt_domain.model.aggregates.tenant.tenant_registrar import TenantWasRegistered
from bookt_domain.model.aggregates.user.user_email_verifier import (
    UserEmailVerifier,
    UserEmailWasVerified,
)
from bookt_domain.model.aggregates.user.user_password_manager import UserPasswordManager
from bookt_domain.model.aggregates.user.user_registrar import (
    UserRegistrar,
    UserWasRegistered,
)

logger = structlog.get_logger()


async def create_tenant_email_verifier(
    unit_of_work: UnitOfWork,
    event: TenantWasRegistered,
):
    tenant_email_verifier = TenantEmailVerifier()
    tenant_email_verifier.create(tenant_id=event.tenant_id)

    await unit_of_work.repository.save(aggregate=tenant_email_verifier)


async def add_eligible_tenant_to_user_registrar(
    unit_of_work: UnitOfWork,
    event: TenantEmailWasVerified,
):
    registrar = await unit_of_work.repository.get_singleton(
        aggregate_root_class=UserRegistrar,
    )

    registrar.add_eligible_tenant_id(tenant_id=event.tenant_id)

    await unit_of_work.repository.save(aggregate=registrar)


async def create_user_email_verifier(
    unit_of_work: UnitOfWork,
    event: UserWasRegistered,
):
    user_email_verifier = UserEmailVerifier()
    user_email_verifier.create(user_id=event.user_id)

    await unit_of_work.repository.save(aggregate=user_email_verifier)


async def create_user_password_manager(
    unit_of_work: UnitOfWork,
    event: UserEmailWasVerified,
):
    password_manager = UserPasswordManager()
    password_manager.create(user_id=event.user_id)

    await unit_of_work.repository.save(aggregate=password_manager)


EVENT_HANDLERS = {
    "TenantWasRegistered": [create_tenant_email_verifier],
    "TenantEmailWasVerified": [add_eligible_tenant_to_user_registrar],
    "UserEmailWasVerified": [create_user_password_manager],
    "UserWasRegistered": [create_user_email_verifier],
}
