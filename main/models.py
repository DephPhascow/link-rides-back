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
    TAXI = 'TAXI', 'Такси'
    REST = 'REST', 'Отдых'
    
class UserManager(BaseUserManager):
    def create_user(self, tg_id, password=None, **extra_fields):
        if not tg_id:
            raise ValueError("The tg_id field must be set")
        user = self.model(tg_id=tg_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, tg_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(tg_id, password, **extra_fields)

class UserModel(AbstractBaseUser, PermissionsMixin):
    tg_id = models.CharField(verbose_name = "TG ID", max_length=100, unique=True)
    password = models.CharField(verbose_name='Пароль', max_length=100)
    first_name = models.CharField(verbose_name='Имя', max_length=50, blank=True, null=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50, blank=True, null=True)    
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_active = models.BooleanField(default=True)
    user_status = models.CharField(
        verbose_name='Статус',
        max_length=50,
        choices=UserStatus.choices,
        default=UserStatus.UNLEGAL
    )
    balance = models.DecimalField(verbose_name='Баланс', max_digits=10, decimal_places=2, default=0.00)    

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
        return f'{self.first_name} {self.last_name}'


class DrivingModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='drivings', verbose_name='Пользователь')
    starting_at = models.DateTimeField(verbose_name='Начало')
    latitude = models.DecimalField(verbose_name='Широта', max_digits=9, decimal_places=6)
    longitude = models.DecimalField(verbose_name='Долгота', max_digits=9, decimal_places=6)
    status = models.CharField(
        verbose_name='Статус',
        max_length=10,
        choices=DrivingStatus.choices
    )

    class Meta:
        verbose_name = "Вождение"
        verbose_name_plural = "Вождения"

    def __str__(self):
        return f"Вождение {self.id} пользователем {self.user.tg_id}"


class TaxiModel(models.Model):
    passenger = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='taxis', verbose_name='Пассажир')
    taxi = models.ForeignKey(DrivingModel, on_delete=models.CASCADE, related_name='taxi_drivings', verbose_name='Такси')
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