import structlog
from cosmos import UnitOfWork

from bookt_domain.model.tenant import TenantRegistered

# from bookt_domain.model.user import User, UserCreated, UserRoles

logger = structlog.get_logger()


async def registration_handler(
    unit_of_work: UnitOfWork,
    event: TenantRegistered,
):
    """..."""

    logger.info("WOOO FROM EVENT")


EVENT_HANDLERS = {
    # Possible to have keys wh/ are invalid events?
    "TenantRegistered": [registration_handler],
    "UserCreated": [],
}
