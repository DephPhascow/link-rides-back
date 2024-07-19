import asyncio
from typing import Optional
from uuid import uuid4
from gqlauth.user import arg_mutations as mutations
import strawberry
from asgiref.sync import sync_to_async

from main.graphql.permissions import IsAuthenticated
from main.graphql.types import UserModelType
from main.models import UserModel

@strawberry.type
class Mutation:
    verify_token = mutations.VerifyToken.field
    token_auth = mutations.ObtainJSONWebToken.field
    refresh_token = mutations.RefreshToken.field
    revoke_token = mutations.RevokeToken.field
    
    @strawberry.mutation
    @sync_to_async
    def get_password_or_create(self, info, tg_id: str, first_name: Optional[str] = None, last_name: Optional[str] = None, username: Optional[str] = None) -> str:
        #TODO check is our server
        password = f"{uuid4()}"
        try:
            user = UserModel.objects.get(tg_id=tg_id)
            user.set_password(password)
            user.save()
            return password
        except UserModel.DoesNotExist:
            user = UserModel.objects.create(tg_id=tg_id, first_name=first_name, last_name=last_name, username=username)
            user.set_password(password)
            user.save()
            return password
        except Exception as e:
            return str(e)
        
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def update_user(self, info: strawberry.Info, first_name: Optional[str] = None, last_name: Optional[str] = None, username: Optional[str] = None) -> UserModelType:
        #TODO if real username set None
        user: UserModel = info.context["request"].user
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if username:
            user.username = username
        user.save()
        return user