from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import Group



gettext = lambda s: s



class UserStatus(models.TextChoices):
    LEGAL = 'LEGAL', 'Легальный'
    UNLEGAL = 'UNLEGAL', 'Нелегальный'


class DrivingStatus(models.TextChoices):
    WAIT = 'WAIT', 'Ожидание'
    DRIVE = 'DRIVE', 'Движение'
    REST = 'REST', 'Отдых'
    
class CarColorEnum(models.TextChoices):
    BLACK = 'BLACK', 'Черный'
    WHITE = 'WHITE', 'Белый'
    
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
    password = models.CharField(verbose_name='Пароль', max_length=100)
    first_name = models.CharField(verbose_name='Имя', max_length=50, blank=True, null=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50, blank=True, null=True)    
    username = models.CharField(verbose_name='Username', max_length=100, blank=True, null=True)
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

    


class TaxiInfoModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='taxi_infos', verbose_name='Пользователь', unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
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
    latitude = models.DecimalField(verbose_name='Широта', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(verbose_name='Долгота', max_digits=9, decimal_places=6, null=True, blank=True)
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
    


class TaxiModel(models.Model):
    passenger = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='taxis', verbose_name='Пассажир')
    taxi = models.ForeignKey(TaxiInfoModel, on_delete=models.CASCADE, related_name='taxi_drivings', verbose_name='Такси')
    from_latitude = models.DecimalField(verbose_name='Широта отправления', max_digits=9, decimal_places=6)
    from_longitude = models.DecimalField(verbose_name='Долгота отправления', max_digits=9, decimal_places=6)
    to_latitude = models.DecimalField(verbose_name='Широта прибытия', max_digits=9, decimal_places=6)
    to_longitude = models.DecimalField(verbose_name='Долгота прибытия', max_digits=9, decimal_places=6)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    taxi_driving_at = models.DateTimeField(verbose_name='Время в пути', blank=True, null=True)
    finish_at = models.DateTimeField(verbose_name='Время окончания', blank=True, null=True)

    class Meta:
        verbose_name = "Такси"
        verbose_name_plural = "Такси"

    def __str__(self):
        return f"Поездка на такси {self.pk} пассажиром {self.passenger.tg_id}"