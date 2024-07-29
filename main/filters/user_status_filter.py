from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Value, Case, When, CharField
from main.models import UserModel

class UserStatusFilter(admin.SimpleListFilter):
    title = _('Выбрать Статус')
    parameter_name = 'user_status'

    def lookups(self, request, model_admin):
        return (
            ('LEGAL', _('Легальный')),
            ('UNLEGAL', _('Не легальный')),
        )

    def queryset(self, request, queryset):
        return queryset.filter(taxi_infos__isnull=False) if self.value() == "LEGAL" else queryset.filter(taxi_infos__isnull=True)
        return filter(lambda x: hasattr(x, 'taxi_infos'), queryset) if self.value() == "LEGAL" else filter(lambda x: not hasattr(x, 'taxi_infos'), queryset)
        if not self.value():
            return queryset.annotate(
                user_status=Case(
                    When(taxi_infos__isnull=False, then=Value('LEGAL')),
                    default=Value('UNLEGAL'),
                    output_field=CharField(),
                )
            )
        if self.value().upper() == 'LEGAL':
            return queryset.annotate(
                user_status=Case(
                    When(taxi_infos__isnull=False, then=Value('LEGAL')),
                    default=Value('UNLEGAL'),
                    output_field=CharField(),
                )
            ).filter(user_status='LEGAL')
        if self.value().upper() == 'UNLEGAL':
            return queryset.annotate(
                user_status=Case(
                    When(taxi_infos__isnull=False, then=Value('LEGAL')),
                    default=Value('UNLEGAL'),
                    output_field=CharField(),
                )
            ).filter(user_status='UNLEGAL')
