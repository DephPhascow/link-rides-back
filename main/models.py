from django.db import models
from ool import VersionField, VersionedMixin
from tinymce.models import HTMLField
from django.contrib.auth.models import AbstractUser, Group, Permission

from main.managers import TmpCustomManager

gettext = lambda s: s


class UserModel(AbstractUser):
    tg_id = models.CharField(verbose_name='Telegram ID', max_length=50, unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=50, blank=True, null=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50, blank=True, null=True)
    join_at = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    status = models.CharField(
        verbose_name='Статус',
        max_length=10,
        choices=[('LEGAL', 'Легальный'), ('UNLEGAL', 'Нелегальный')],
        default='UNLEGAL'
    )
    balance = models.DecimalField(verbose_name='Баланс', max_digits=10, decimal_places=2, default=0.00)

    USERNAME_FIELD = 'tg_id'
    REQUIRED_FIELDS = ['username', 'password']

    groups = models.ManyToManyField(
        Group,
        verbose_name='Группы',
        blank=True,
        help_text="Группы, к которым принадлежит этот пользователь. Пользователь получит все разрешения, предоставленные каждой из его групп.",
        related_name='user_model_groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="Права",
        blank=True,
        help_text="Конкретные разрешения для этого пользователя.",
        related_name='user_model_user_permissions',
        related_query_name='user',
    )    

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class DrivingModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='drivings', verbose_name='Пользователь')
    starting_at = models.DateTimeField(verbose_name='Начало')
    latitude = models.DecimalField(verbose_name='Широта', max_digits=9, decimal_places=6)
    longitude = models.DecimalField(verbose_name='Долгота', max_digits=9, decimal_places=6)
    status = models.CharField(
        verbose_name='Статус',
        max_length=10,
        choices=[('WAIT', 'Ожидание'), ('DRIVE', 'Движение'), ('TAXI', 'Такси'), ('REST', 'Отдых')]
    )

    class Meta:
        verbose_name = "Вождение"
        verbose_name_plural = "Вождения"

    def __str__(self):
        return f"Вождение {self.id} пользователем {self.user.username}"


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
        return f"Поездка на такси {self.id} пассажиром {self.passenger.username}"


class TmpRoleEnum(models.TextChoices):
    SIMPLE = "SIMPLE", gettext("Простой")
    ADVANCED = "ADVANCED", gettext("Продвинутый")


class TmpModel(VersionedMixin, models.Model):
    name = models.CharField(max_length=100, verbose_name=gettext("Название"))
    description = HTMLField(max_length=100, verbose_name=gettext("Описание"))
    role = models.CharField(max_length=100, choices=TmpRoleEnum.choices, verbose_name=gettext("Роль"), default=TmpRoleEnum.SIMPLE)
    image = models.ImageField(upload_to='images/', verbose_name=gettext("Изображение"), blank=True, null=True)
    version = VersionField()
    custom_manager = TmpCustomManager()
    objects = models.Manager()

    class Meta:
        verbose_name = "TmpModel"
        verbose_name_plural = "TmpModels"
        base_manager_name = 'custom_manager'    

    def __str__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)
