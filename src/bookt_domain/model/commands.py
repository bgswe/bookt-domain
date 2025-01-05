from uuid import UUID

from cosmos.domain import Command


class RegisterTenant(Command):
    tenant_id: UUID | None = None
    tenant_name: str
    tenant_registration_email: str


class VerifyTenantEmail(Command):
    verification_key: str


class RegisterUser(Command):
    tenant_id: UUID
    user_id: UUID | None = None
    email: str


class VerifyUserEmail(Command):
    verification_key: str


class SetUserPassword(Command):
    set_password_key: str
    password: str


class AuthenticateUser(Command):
    user_authenticator_id: UUID
    password: str
