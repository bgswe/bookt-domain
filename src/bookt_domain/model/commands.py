from uuid import UUID

from cosmos.domain import Command


class RegisterTenant(Command):
    tenant_id: UUID | None = None
    tenant_name: str


class RegisterUser(Command):
    user_id: UUID | None = None
    tenant_id: UUID
    email: str
    password: str
    first_name: str
    last_name: str
