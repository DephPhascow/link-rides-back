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
        instance = GlobalConstant.objects.filter(key="PAYMENT_FOR_ARRIVAL")
        if not instance:
            GlobalConstant.objects.create(
                key="PAYMENT_FOR_ARRIVAL", key_type=KeyTypeChoices.FLOAT, value=5_000 #
            )
        instance = GlobalConstant.objects.filter(key="BALL_FOR_REFERRAL")
        if not instance:
            GlobalConstant.objects.create(
                key="BALL_FOR_REFERRAL", key_type=KeyTypeChoices.FLOAT, value=2 #
            )