import asyncio
from gqlauth.user import arg_mutations as mutations
import strawberry
from asgiref.sync import async_to_sync, sync_to_async
from main.graphql.types import TmpType
from main.models import TmpModel
from django.core.serializers import deserialize, serialize

@strawberry.type
class Mutation:
    verify_token = mutations.VerifyToken.field
    update_account = mutations.UpdateAccount.field
    archive_account = mutations.ArchiveAccount.field
    delete_account = mutations.DeleteAccount.field
    password_change = mutations.PasswordChange.field
    token_auth = mutations.ObtainJSONWebToken.field
    register = mutations.Register.field
    verify_account = mutations.VerifyAccount.field
    resend_activation_email = mutations.ResendActivationEmail.field
    send_password_reset_email = mutations.SendPasswordResetEmail.field
    password_reset = mutations.PasswordReset.field
    password_set = mutations.PasswordSet.field
    refresh_token = mutations.RefreshToken.field
    revoke_token = mutations.RevokeToken.field
    @strawberry.mutation
    def add_tmp(self, info, name: str, description: str) -> str:
        instance = TmpModel(
            name=name,
            description=description
        )
        instance.save()
        asyncio.run(info.context.broadcast.publish(
            channel="heros", message=serialize("json", [instance])
        ))
        return "heree"