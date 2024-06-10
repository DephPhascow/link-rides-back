import strawberry
from .types import TmpType
from .permissions import IsAuthenticated
from gqlauth.user.queries import UserQueries

@strawberry.type
class Query(UserQueries):
    tmps: list[TmpType] = strawberry.django.field(permission_classes=[IsAuthenticated], )