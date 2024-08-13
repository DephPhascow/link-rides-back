from typing import Optional
import strawberry
import strawberry_django
from strawberry import auto
from main import models
from main.graphql import filters, orders

@strawberry_django.type(models.UserModel, fields="__all__", pagination=True, )
class UserModelType:
    id: auto
    referrer: Optional["UserModelType"]
    get_taxi_infos: Optional["TaxiInfoModelType"]
    count_balls: int

    
@strawberry_django.type(models.TaxiInfoModel, fields="__all__", pagination=True, )
class TaxiInfoModelType:
    id: auto
    user: UserModelType

@strawberry_django.type(models.TaxiModel, fields="__all__", pagination=True, )
class TaxiModelType:
    id: auto
    passenger: UserModelType
    taxi: TaxiInfoModelType
    price: float
    
@strawberry_django.type(models.TariffModel, fields="__all__", pagination=True, )
class TariffModelType:
    id: auto
    
@strawberry_django.type(models.TaxiConfirmationApplicationModel, fields="__all__", pagination=True, )
class TaxiConfirmationApplicationModelType:
    id: auto
    
@strawberry.type
class SettingsType:
    cost_per_km: float