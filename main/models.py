from decimal import Decimal
import math
from typing import Dict, List, Optional, Tuple, Union
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import Group
from geopy.distance import geodesic
from django_constants.models import GlobalConstant

gettext = lambda s: s



class UserStatus(models.TextChoices):
    LEGAL = 'LEGAL', 'Легальный'
    UNLEGAL = 'UNLEGAL', 'Нелегальный'


class DrivingStatus(models.TextChoices):
    WAIT = 'WAIT', 'Ожидание'
    DRIVE = 'DRIVE', 'Движение'
    REST = 'REST', 'Отдых'
    
class ApplicationStatusEnum(models.TextChoices):
    WAIT = 'WAIT', 'Ожидание'
    TAXI_ACCEPTED = 'TAXI_ACCEPTED', 'Такси принял заказ'
    DRIVE = 'DRIVE', 'Движение'
    FINISH = 'FINISH', 'Завершено'
    CANCELED = 'CANCELED', 'Отменено'
    
class CarColorEnum(models.TextChoices):
    BLACK = 'BLACK', 'Черный'
    WHITE = 'WHITE', 'Белый'

class BallTypeEnum(models.TextChoices):
    REFERRAL = 'REFERRAL', 'Реферал'
    DRIVE = 'DRIVE', 'Поездка'
    
class UserManager(BaseUserManager):
    def create_user(self, tg_id: str, password=None, **extra_fields):
        if not tg_id:
            raise ValueError("The tg_id field must be set")
        user = self.model(tg_id=tg_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, tg_id: str, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(tg_id, password, **extra_fields)

class UserModel(AbstractBaseUser, PermissionsMixin):
    tg_id = models.CharField(verbose_name = "TG ID", max_length=100, unique=True)
    referrer = models.ForeignKey("self", on_delete=models.SET_NULL, related_name='referrals', verbose_name='Реферал', null=True, blank=True)
    password = models.CharField(verbose_name='Пароль', max_length=100)
    first_name = models.CharField(verbose_name='Имя', max_length=50, blank=True, null=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50, blank=True, null=True)    
    username = models.CharField(verbose_name='Username', max_length=100, blank=True, null=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=20, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, blank=True)

    USERNAME_FIELD = "tg_id"
    EMAIL_FIELD = "tg_id"
    REQUIRED_FIELDS = []
    email = None

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.tg_id})'

    @property
    def user_status(self):
        if hasattr(self, 'taxi_infos') and self.taxi_infos:
            return UserStatus.LEGAL
        return UserStatus.UNLEGAL
    def get_taxi_infos(self) -> Optional["TaxiInfoModel"]:
        return getattr(self, 'taxi_infos', None)
    
    def count_balls(self) -> int:
        return sum([x.count for x in self.balls.all()])

class BallModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='balls', verbose_name='Пользователь')
    ball_type = models.CharField(
        verbose_name='Тип баллов',
        max_length=50,
        choices=BallTypeEnum.choices,
    )
    count = models.PositiveIntegerField(verbose_name='Количество')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)


class TaxiInfoModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='taxi_infos', verbose_name='Пользователь', unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    tariff = models.ForeignKey('TariffModel', on_delete=models.CASCADE, related_name='taxi_infos', verbose_name='Тариф', null=True, blank=True)
    car_brand = models.CharField(verbose_name='Марка машины', max_length=100)
    car_model = models.CharField(verbose_name='Модель машины', max_length=100)
    car_color = models.CharField(verbose_name='Цвет машины', max_length=10, choices=CarColorEnum.choices)
    car_number = models.CharField(verbose_name='Номер машины', max_length=10)
    year = models.IntegerField(verbose_name='Год выпуска')
    series_license = models.CharField(verbose_name='Серия лицензии', max_length=10)
    country_license = models.CharField(verbose_name='Страна лицензии', max_length=50)
    date_get_license = models.DateField(verbose_name='Дата получения')
    license_valid_until = models.DateField(verbose_name='Действительно до')
    photo_license = models.ImageField(verbose_name='Фото лицензии', upload_to='license/', null=True, blank=True)
    starting_at = models.DateTimeField(auto_now_add=True, verbose_name='Начало', null=True, blank=True)
    latitude = models.FloatField(verbose_name='Широта', null=True, blank=True)
    longitude = models.FloatField(verbose_name='Долгота', null=True, blank=True)
    status = models.CharField(
        verbose_name='Статус',
        max_length=35,
        choices=DrivingStatus.choices,
        default=DrivingStatus.REST
    )
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)    
    class Meta:
        verbose_name = "Информация о такси"
        verbose_name_plural = "Информация о такси"

    def __str__(self):
        return f"Информация о такси {self.user.tg_id}"
    
    def find_nearby_taxis(client_coords: Tuple[float, float], tariff: "TariffModel", max_distance=10):  
        """  
        Находит таксистов, находящихся в пределах max_distance метров от координат клиента.  
        
        :param client_coords: Кортеж с координатами клиента (широта, долгота)  
        :param max_distance: Максимальное расстояние в метрах  
        :return: Список таксистов, находящихся в пределах max_distance  
        """  
        nearby_taxis: List[Dict[str, Union[TaxiInfoModel, float]]] = []  
        taxis = TaxiInfoModel.objects.filter(tariff=tariff, status = DrivingStatus.WAIT)
        for taxi in taxis:  
            if taxi.latitude is not None and taxi.longitude is not None:  
                taxi_coords = (taxi.latitude, taxi.longitude)  
                distance = geodesic(client_coords, taxi_coords).meters  
                if distance <= max_distance:  
                    nearby_taxis.append({  
                        'taxi': taxi,  
                        'distance': distance  
                    })  

        return nearby_taxis  
    
    def has_current_application(self) -> bool:
        return TaxiModel.objects.filter(taxi=self, status__in=[ApplicationStatusEnum.TAXI_ACCEPTED, ApplicationStatusEnum.DRIVE]).exists()
    


class TaxiModel(models.Model):
    passenger = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='taxis', verbose_name='Пассажир')
    taxi = models.ForeignKey(TaxiInfoModel, on_delete=models.CASCADE, related_name='taxi_drivings', verbose_name='Такси', null=True, blank=True)
    need_tariff = models.ForeignKey('TariffModel', on_delete=models.CASCADE, related_name='taxi_drivings', verbose_name='Требуется тариф') ### TODO по окончании сделать как обязательным
    from_latitude = models.FloatField(verbose_name='Широта отправления')
    from_longitude = models.FloatField(verbose_name='Долгота отправления')
    to_latitude = models.FloatField(verbose_name='Широта прибытия', null=True, blank=True )
    to_longitude = models.FloatField(verbose_name='Долгота прибытия', null=True, blank=True)
    from_address = models.CharField(verbose_name='Адрес отправления', max_length=255,)
    to_address = models.CharField(verbose_name='Адрес прибытия', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    taxi_driving_at = models.DateTimeField(verbose_name='Время в пути', blank=True, null=True)
    finish_at = models.DateTimeField(verbose_name='Время окончания', blank=True, null=True)
    status = models.CharField(
        verbose_name='Статус',
        max_length=50,
        choices=ApplicationStatusEnum.choices,
        default=ApplicationStatusEnum.WAIT
    )
    class Meta:
        verbose_name = "Такси"
        verbose_name_plural = "Такси"

    def __str__(self):
        return f"Поездка на такси {self.pk} пассажиром {self.passenger.tg_id}"
    
    @property
    def price(self) -> float:
        if not self.need_tariff:
            return 0
        tariff: "TariffModel" = self.need_tariff
        cost_per_km = tariff.per_one_km
        PAYMENT_FOR_ARRIVAL = tariff.per_one_km_before ### TODO * на время 
        price = cost_per_km
        if self.to_latitude and self.to_longitude:
            distance = geodesic((self.from_latitude, self.from_longitude), (self.to_latitude, self.to_longitude)).km
            price = distance * cost_per_km
        return math.ceil(price + float(PAYMENT_FOR_ARRIVAL))
    
class TariffModel(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    per_one_km = models.FloatField(verbose_name='Цена за км', default=0)
    per_one_km_before = models.FloatField(verbose_name='Цена за км до', default=0)
    is_available = models.BooleanField(verbose_name='Доступен', default=True)
    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
    def __str__(self) -> str:
        return f'{self.name} ({self.is_available})'
    
class TaxiConfirmationApplicationModel(models.Model):
    application = models.OneToOneField(TaxiModel, on_delete=models.CASCADE, related_name='taxi_confirmation_applications', verbose_name='Поездка на такси')
    taxies = models.ManyToManyField(TaxiInfoModel, related_name='taxi_confirmation_applications', verbose_name='Такси')    
    class Meta:
        verbose_name = "Ожидание принятие заказа"
        verbose_name_plural = "Ожидание принятие заказа"
    def __str__(self) -> str:
        return f'{self.application}'