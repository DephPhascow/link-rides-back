import asyncio
from gqlauth.user import arg_mutations as mutations
import strawberry
from asgiref.sync import sync_to_async

@strawberry.type
class Mutation:
    verify_token = mutations.VerifyToken.field
    token_auth = mutations.ObtainJSONWebToken.field
    refresh_token = mutations.RefreshToken.field
    revoke_token = mutations.RevokeToken.field
    
    # @strawberry.mutation
    # def add_tmp(self, info, name: str, description: str) -> str:
    #     instance = TmpModel(
    #         name=name,
    #         description=description
    #     )
    #     instance.save()
    #     asyncio.run(info.context.broadcast.publish(
    #         channel="heros", message=serialize("json", [instance])
    #     ))
    #     return "heree"