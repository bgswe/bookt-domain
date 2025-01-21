import structlog
from cosmos import UnitOfWork, event

from bookt_domain.model.aggregates.tenant.tenant_email_verifier import (
    TenantEmailVerifier,
    TenantEmailWasVerified,
)
from bookt_domain.model.aggregates.tenant.tenant_registrar import TenantWasRegistered
from bookt_domain.model.aggregates.user.user_authenticator import UserAuthenticator
from bookt_domain.model.aggregates.user.user_email_verifier import (
    UserEmailVerifier,
    UserEmailWasVerified,
)
from bookt_domain.model.aggregates.user.user_registrar import (
    UserRegistrar,
    UserWasRegistered,
)

logger = structlog.get_logger()


@event(event_type_name="TenantWasRegistered")
async def create_tenant_email_verifier(
    unit_of_work: UnitOfWork,
    event: TenantWasRegistered,
):
    tenant_email_verifier = TenantEmailVerifier()
    tenant_email_verifier.create(tenant_id=event.tenant_id)

    await unit_of_work.repository.save(aggregate=tenant_email_verifier)


@event(event_type_name="TenantEmailWasVerified")
async def add_eligible_tenant_to_user_registrar(
    unit_of_work: UnitOfWork,
    event: TenantEmailWasVerified,
):
    registrar = await unit_of_work.repository.get_singleton(
        aggregate_root_class=UserRegistrar,
    )

    registrar.add_eligible_tenant_id(tenant_id=event.tenant_id)

    await unit_of_work.repository.save(aggregate=registrar)


@event(event_type_name="UserWasRegistered")
async def create_user_email_verifier(
    unit_of_work: UnitOfWork,
    event: UserWasRegistered,
):
    user_email_verifier = UserEmailVerifier()
    user_email_verifier.create(user_id=event.user_id)

    await unit_of_work.repository.save(aggregate=user_email_verifier)


@event(event_type_name="UserEmailWasVerified")
async def create_user_password_manager(
    unit_of_work: UnitOfWork,
    event: UserEmailWasVerified,
):
    authenticator = UserAuthenticator()
    authenticator.create(user_id=event.user_id)
    authenticator.generate_set_password_key()

    await unit_of_work.repository.save(aggregate=authenticator)
