from uuid import UUID

from cosmos.domain import Command


class RegisterTenant(Command):
    tenant_id: UUID | None = None
    tenant_name: str
