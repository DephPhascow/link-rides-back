import strawberry_django
# from .types import TmpType
from .permissions import IsAuthenticated
from gqlauth.user.queries import UserQueries
import strawberry

@strawberry.type
class Query(UserQueries):
    pass
    # tmps: list[TmpType] = strawberry_django.field(permission_classes=[IsAuthenticated], )