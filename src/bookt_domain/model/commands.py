from uuid import UUID

from cosmos.domain import Command


class RegisterTenant(Command):
    tenant_registration_id: UUID | None = None
    tenant_id: UUID | None = None
    tenant_name: str
    tenant_registration_email: str


class ValidateTenantEmail(Command):
    tenant_registration_id: UUID


class RegisterUser(Command):
    user_registration_id: UUID | None = None
    user_id: UUID | None = None
    tenant_id: UUID
    email: str
    password: str
