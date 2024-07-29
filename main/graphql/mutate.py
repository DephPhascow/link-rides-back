import asyncio
from typing import Optional
from uuid import uuid4
from gqlauth.user import arg_mutations as mutations
import strawberry
from asgiref.sync import sync_to_async

from main.graphql.inputs import TaxiInfoInput
from main.graphql.permissions import IsAuthenticated
from main.graphql.types import TaxiInfoModelType, UserModelType
from main.graphql.enums import DrivingStatus
from main.models import TaxiInfoModel, UserModel

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
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def create_taxi_info_data(self, info: strawberry.Info, data: TaxiInfoInput) -> TaxiInfoModelType:
        user: UserModel = info.context["request"].user
        taxi_infos = user.get_taxi_infos()
        if taxi_infos:
            raise Exception("Произошла ошибка, у вас уже есть данные таксиста")
        instance = TaxiInfoModel.objects.create(
            user=user, 
            first_name=data.first_name, 
            last_name=data.last_name, 
            car_brand=data.car_brand, 
            car_model=data.car_model, 
            car_color=data.car_color, 
            car_number=data.car_number, 
            year=data.year, 
            series_license=data.series_license, 
            date_get_license = data.date_get_license,
            country_license=data.country_license, 
            license_valid_until=data.license_valid_until, 
            # photo_license=data.photo_license, 
        )
        ### TODO загрузить фотку
        return instance
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def taxi_set_my_current_location(self, info: strawberry.Info, latitude: float, longitude: float, status: DrivingStatus = None) -> TaxiInfoModelType:
        user: UserModel = info.context["request"].user
        taxi_infos = user.get_taxi_infos()
        if not taxi_infos:
            raise Exception("Вы не являетесь таксистом")
        taxi_infos.latitude = latitude
        taxi_infos.longitude = longitude
        if status:
            taxi_infos.status = status
        taxi_infos.save()
        return taxi_infos
    
