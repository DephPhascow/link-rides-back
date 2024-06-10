from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class TmpFilter(admin.SimpleListFilter):
    title = _('Выбрать tmp')
    parameter_name = 'choice_tmp'
    def lookups(self, request, model_admin):
        return (
            ('A', _('A')),
            ('B', _('B')),
        )
    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.filter(name__icontains=self.value())