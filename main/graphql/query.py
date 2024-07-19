from typing import List
import strawberry_django

from main.graphql.enums import UserDriveType
from main.graphql.types import SettingsType, TaxiModelType
from main.models import DrivingModel, TaxiModel
# from .types import TmpType
from .permissions import IsAuthenticated
from gqlauth.user.queries import UserQueries
import strawberry
from asgiref.sync import sync_to_async
from django_constants.models import GlobalConstant

@strawberry.type
class Query(UserQueries):
    pass
    # tmps: list[TmpType] = strawberry_django.field(permission_classes=[IsAuthenticated], )
    
    @strawberry_django.field(permission_classes=[IsAuthenticated], )
    async def settings(self, info) -> SettingsType:
        return SettingsType(
            cost_per_km = (await sync_to_async(GlobalConstant.objects.get)(key="COST_PER_KM")).value
        )
    
    @strawberry.field(permission_classes=[IsAuthenticated], )
    async def history(self, info, type: UserDriveType) -> List[TaxiModelType]:
        user = info.context["request"].user
        kwargs = {}
        if type == UserDriveType.TAXI:
            taxi = await sync_to_async(DrivingModel.objects.get)(user=user)
            kwargs["taxi"] = taxi
        else:
            kwargs["passenger"] = user
        return await sync_to_async(lambda: list(TaxiModel.objects.filter(**kwargs)))()