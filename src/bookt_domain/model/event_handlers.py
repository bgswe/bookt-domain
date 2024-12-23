import structlog
from cosmos import UnitOfWork

from bookt_domain.model.tenant_email_validator import (
    TenantEmailValidator,
    TenantEmailWasValidated,
)
from bookt_domain.model.tenant_registrar import TenantWasRegistered
from bookt_domain.model.user_registrar import UserRegistrar

logger = structlog.get_logger()


async def create_tenant_email_validator_for_tenant(
    unit_of_work: UnitOfWork,
    event: TenantWasRegistered,
):
    tenant_email_validator = TenantEmailValidator()
    tenant_email_validator.create(tenant_id=event.tenant_id)

    await unit_of_work.repository.save(aggregate=tenant_email_validator)


async def add_eligible_tenant_to_user_registrar(
    unit_of_work: UnitOfWork,
    event: TenantEmailWasValidated,
):
    registrar = await unit_of_work.repository.get_singleton(
        aggregate_root_class=UserRegistrar,
    )

    registrar.add_eligible_tenant_id(tenant_id=event.tenant_id)

    await unit_of_work.repository.save(aggregate=registrar)


EVENT_HANDLERS = {
    "TenantWasRegistered": [create_tenant_email_validator_for_tenant],
    "TenantEmailWasValidated": [add_eligible_tenant_to_user_registrar],
}
