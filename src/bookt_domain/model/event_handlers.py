import structlog
from cosmos import UnitOfWork

from bookt_domain.model.tenant_registratrar import TenantRegistrationIsComplete
from bookt_domain.model.user_registrar import UserRegistrar

logger = structlog.get_logger()


async def create_user_registrar_on_tenant_registration(
    unit_of_work: UnitOfWork,
    event: TenantRegistrationIsComplete,
):
    """Initiates the registration process for a User"""

    user_registrar = UserRegistrar()
    user_registrar = user_registrar.create(tenant_id=event.tenant_id)

    await unit_of_work.repository.save(aggregate=user_registrar)


EVENT_HANDLERS = {
    "TenantRegistrationIsComplete": [create_user_registrar_on_tenant_registration],
}
