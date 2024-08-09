import asyncio
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4
from gqlauth.user import arg_mutations as mutations
import strawberry
from asgiref.sync import sync_to_async
import requests
from main.graphql.inputs import TaxiInfoInput
from main.graphql.permissions import IsAuthenticated
from main.graphql.types import TaxiConfirmationApplicationModelType, TaxiInfoModelType, TaxiModelType, UserModelType
from main.graphql.enums import DrivingStatus
from main.models import ApplicationStatusEnum, TariffModel, TaxiConfirmationApplicationModel, TaxiInfoModel, TaxiModel, UserModel
from geopy.geocoders import Nominatim

@strawberry.type
class Mutation:
    verify_token = mutations.VerifyToken.field
    token_auth = mutations.ObtainJSONWebToken.field
    refresh_token = mutations.RefreshToken.field
    revoke_token = mutations.RevokeToken.field
    
    @strawberry.mutation
    @sync_to_async
    def get_password_or_create(self, info, tg_id: str, first_name: Optional[str] = None, last_name: Optional[str] = None, username: Optional[str] = None, phone_number: Optional[str] = None) -> str:
        #TODO check is our server
        password = f"{uuid4()}"
        try:
            user = UserModel.objects.get(tg_id=tg_id)
            user.set_password(password)
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if username:
                user.username = username
            if phone_number:
                user.phone_number = phone_number
            user.save()
            return password
        except UserModel.DoesNotExist:
            user = UserModel.objects.create(tg_id=tg_id, first_name=first_name, last_name=last_name, username=username)
            user.set_password(password)
            user.phone_number = phone_number
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
    def taxi_set_my_current_location(self, info: strawberry.Info, latitude: float, longitude: float, status: Optional[DrivingStatus] = None) -> TaxiInfoModelType:
        user: UserModel = info.context["request"].user
        taxi_infos = user.get_taxi_infos()
        if not taxi_infos:
            raise Exception("Вы не являетесь таксистом")
        taxi_infos.latitude = latitude
        taxi_infos.longitude = longitude
        if status:
            taxi_infos.status = status.value
        taxi_infos.save()
        return taxi_infos

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def taxi_set_status(self, info: strawberry.Info, status: DrivingStatus) -> TaxiInfoModelType:
        user: UserModel = info.context["request"].user
        taxi_infos = user.get_taxi_infos()
        if not taxi_infos:
            raise Exception("Вы не являетесь таксистом")
        ### TODO есть ли клиент сейчас у него
        taxi_infos.status = status.value
        taxi_infos.save()
        return taxi_infos
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def find_taxi(self, info: strawberry.Info, tariff_id: int, from_latitude: float, from_longitude: float, to_latitude: Optional[float] = None, to_longitude: Optional[float] = None) -> TaxiModelType:
        geolocator = Nominatim(user_agent="linkrides-bot")
        user: UserModel = info.context["request"].user
        need_tariff = TariffModel.objects.get(id=tariff_id)
        from_address = geolocator.reverse((from_latitude, from_longitude)).address,
        to_address = geolocator.reverse((to_latitude, to_longitude)).address,        
        instance = TaxiModel.objects.create(
            passenger=user,
            need_tariff = need_tariff,
            from_latitude=from_latitude,
            from_longitude=from_longitude,
            to_latitude=to_latitude,
            to_longitude=to_longitude,
            from_address = from_address,
            to_address = to_address,
        )
        taxis = TaxiInfoModel.find_nearby_taxis((from_latitude, from_longitude), need_tariff)
        if len(taxis) == 0:
            requests.post(
                url = "https://linkrides.uz/bot/api/system/application/cancelled",
                params = {
                    "application_id": instance.pk,
                    "client_id": instance.passenger.tg_id,
                }
            )
            instance.status = ApplicationStatusEnum.CANCELED
            return instance
        for taxi in taxis:
            res = requests.post(
                url = "https://linkrides.uz/bot/api/system/application/new",
                params = {
                    "taxi_id": taxi['taxi'].user.tg_id,
                    "from_latitude": from_latitude,
                    "from_longitude": from_longitude,
                    "price": instance.price,
                    "to_latitude": to_latitude,
                    "to_longitude": to_longitude,
                    "application_id": instance.pk,
                })        
        tmp = TaxiConfirmationApplicationModel.objects.create(
            application=instance,
        )
        tmp.taxies.add(*taxis)
        return instance    

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def taxi_cancel_application(self, info: strawberry.Info, application_id: int) -> bool:
        user: UserModel = info.context["request"].user
        taxi_info = user.get_taxi_infos()
        if not taxi_info:
            raise Exception("Вы не являетесь таксистом")
        instance = TaxiConfirmationApplicationModel.objects.get(application_id=application_id)
        if not instance:
            raise Exception("Заявка не найдена")
        if not instance.taxies.filter(user=taxi_info).exists():
            raise Exception("Вы не можете отклонить этот заказ, так как он не ваш")        
        instance.taxies.remove(user.get_taxi_infos)
        if instance.taxies.count() == 0:
            requests.post(
                url = "https://linkrides.uz/bot/api/system/application/cancelled",
                params = {
                    "application_id": instance.application.pk,
                    "client_id": instance.application.passenger.tg_id,
                }
            )
            instance.application.status = ApplicationStatusEnum.CANCELED
            instance.application.save()
        instance.save()
        return True
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def taxi_accept_application(self, info: strawberry.Info, application_id: int) -> bool:
        user: UserModel = info.context["request"].user
        taxi_info = user.get_taxi_infos()
        if not taxi_info:
            raise Exception("Вы не являетесь таксистом")
        # TODO проверить что такси не опоздал выбор
        instance = TaxiConfirmationApplicationModel.objects.get(application_id=application_id)
        if not instance:
            raise Exception("Заявка не найдена")
        if not instance.taxies.filter(user=taxi_info).exists():
            raise Exception("Вы не можете принять этот заказ")
        
        application = instance.application
        application.taxi = user.get_taxi_infos()
        application.taxi_driving_at = datetime.now(timezone.utc)
        application.status = ApplicationStatusEnum.TAXI_ACCEPTED
        requests.post(
            url = "https://linkrides.uz/bot/api/system/application/accepted",
            params = {
                "application_id": instance.application.pk,
                "client_id": instance.application.passenger.tg_id,
                "taxi_id": taxi_info.pk,
                "current_taxi_latitude": taxi_info.latitude,
                "current_taxi_longitude": taxi_info.longitude,
                "taxi_fio": f"{taxi_info.first_name} {taxi_info.last_name or ''}",
                "car_brand": taxi_info.car_brand,
                "car_model": taxi_info.car_model,
                "car_color": taxi_info.car_color,
                "car_number": taxi_info.car_number,
            }
        )
        instance.delete()   
        return True