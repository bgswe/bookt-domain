from uuid import UUID

from cosmos.domain import Command


class RegisterTenant(Command):
    tenant_id: UUID | None = None
    tenant_name: str
    tenant_registration_email: str


class ValidateTenantEmail(Command):
    validation_key: str


# class RegisterUser(Command):
#     user_registrar_id: UUID
#     email: str
#     user_registration_id: UUID | None = None
#     user_id: UUID | None = None
