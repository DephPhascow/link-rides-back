from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    def ready(self) -> None:
        from django_constants.models import GlobalConstant, KeyTypeChoices
        super().ready()
        instance = GlobalConstant.objects.filter(key="COST_PER_KM")
        if not instance:
            GlobalConstant.objects.create(
                key="COST_PER_KM", key_type=KeyTypeChoices.FLOAT, value=1000 #
            )