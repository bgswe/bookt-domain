from uuid import UUID

from cosmos.domain import Command


class RegisterTenant(Command):
    tenant_id: UUID | None = None
    tenant_name: str
    tenant_registration_email: str


class ValidateTenantEmail(Command):
    validation_key: str


class RegisterUser(Command):
    tenant_id: UUID
    user_id: UUID | None = None
    email: str


class ValidateUserEmail(Command):
    validation_key: str
