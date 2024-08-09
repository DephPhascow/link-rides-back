from typing import List, Optional
import strawberry_django

from main.graphql.enums import TopByEnum, UserDriveType
from main.graphql.types import SettingsType, TariffModelType, TaxiModelType, UserModelType
from main.models import TaxiInfoModel, TaxiModel, UserModel
# from .types import TmpType
from .permissions import IsAuthenticated
from gqlauth.user.queries import UserQueries
import strawberry
from asgiref.sync import sync_to_async
from django_constants.models import GlobalConstant

@strawberry.type
class Query:
    pass
    tariffs: List[TariffModelType] = strawberry_django.field(permission_classes=[IsAuthenticated], )
    # tmps: list[TmpType] = strawberry_django.field(permission_classes=[IsAuthenticated], )
    
    @strawberry_django.field(permission_classes=[IsAuthenticated], )
    async def me(self, info) -> UserModelType:
        return info.context["request"].user
        
    @strawberry_django.field(permission_classes=[IsAuthenticated], )
    async def settings(self, info) -> SettingsType:
        return SettingsType(
            cost_per_km = (await sync_to_async(GlobalConstant.objects.get)(key="COST_PER_KM")).value
        )
    
    @strawberry.field(permission_classes=[IsAuthenticated], )
    async def history(self, info, type: UserDriveType, offset: int, limit: int) -> List[TaxiModelType]:
        user = info.context["request"].user
        kwargs = {}
        if type == UserDriveType.TAXI:
            taxi = await sync_to_async(TaxiInfoModel.objects.get)(user=user)
            kwargs["taxi"] = taxi
        else:
            kwargs["passenger"] = user
        objects = await sync_to_async(lambda: list(TaxiModel.objects.filter(**kwargs)))()
        return objects[offset:offset+limit]
    
    @strawberry.field(permission_classes=[IsAuthenticated], )
    async def history_count(self, info, type: UserDriveType) -> int:
        user = info.context["request"].user
        kwargs = {}
        if type == UserDriveType.TAXI:
            taxi = await sync_to_async(TaxiInfoModel.objects.get)(user=user)
            kwargs["taxi"] = taxi
        else:
            kwargs["passenger"] = user
        return await sync_to_async(TaxiModel.objects.filter(**kwargs).count)()

    @strawberry.field(permission_classes=[IsAuthenticated], )
    async def top(
        self, info: strawberry.Info, top_type: Optional[TopByEnum] = TopByEnum.ALL,
    ) -> List[UserModelType]:
        kwargs = {}
        if top_type == TopByEnum.TAXI:
            kwargs["taxi_infos__isnull"] = False
        elif top_type == TopByEnum.PASSENGER:
            kwargs["taxi_infos__isnull"] = True
        objects = await sync_to_async(lambda: list(UserModel.objects.filter(**kwargs)))()
        return objects[:25]