import strawberry
import strawberry_django
from strawberry import auto
from main import models
from main.graphql import filters, orders

@strawberry_django.type(models.UserModel, fields="__all__", pagination=True, )
class UserModelType:
    id: auto
    
@strawberry_django.type(models.DrivingModel, fields="__all__", pagination=True, )
class DrivingModelType:
    id: auto
    user: UserModelType

@strawberry_django.type(models.TaxiModel, fields="__all__", pagination=True, )
class TaxiModelType:
    id: auto
    passenger: UserModelType
    taxi: DrivingModelType
    
@strawberry.type
class SettingsType:
    cost_per_km: float