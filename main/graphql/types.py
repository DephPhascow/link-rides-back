from typing import Optional
import strawberry
import strawberry_django
from strawberry import auto
from main import models
from main.graphql import filters, orders

@strawberry_django.type(models.UserModel, fields="__all__", pagination=True, )
class UserModelType:
    id: auto
    get_taxi_infos: Optional["TaxiInfoModelType"]
    
@strawberry_django.type(models.TaxiInfoModel, fields="__all__", pagination=True, )
class TaxiInfoModelType:
    id: auto
    user: UserModelType

@strawberry_django.type(models.TaxiModel, fields="__all__", pagination=True, )
class TaxiModelType:
    id: auto
    passenger: UserModelType
    taxi: TaxiInfoModelType
    
@strawberry.type
class SettingsType:
    cost_per_km: float