from django.db import models
from ool import VersionField, VersionedMixin
from tinymce.models import HTMLField
from django.contrib.auth.models import AbstractUser, Group, Permission

from main.managers import TmpCustomManager

gettext = lambda s: s


class UserModel(AbstractUser):
    username = models.CharField(verbose_name='Имя пользователя', max_length=50, unique=True)
    password = models.CharField(verbose_name='Пароль', max_length=50)
    is_superuser = models.BooleanField(verbose_name='Суперпользователь', default=False)
    is_active = models.BooleanField(verbose_name='Активный', default=True)
    date_register = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
    USERNAME_FIELD = 'username'
    groups = models.ManyToManyField(
        Group,
        verbose_name='Группы',
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name='user_model_groups',
    )
    user_permissions = models.ManyToManyField(
            Permission,
            verbose_name="Права",
            blank=True,
            help_text="Specific permissions for this user.",
            related_name='user_model_user_permissions',
            related_query_name='user',
        )    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    def __str__(self):
        return self.username

class TmpRoleEnum(models.TextChoices):
    SIMPLE = "SIMPLE", gettext("Simple")
    ADVANCED = "ADVANCED", gettext("Advanced")

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
    #TmpModel.custom_manager.get_by_name('Deph')