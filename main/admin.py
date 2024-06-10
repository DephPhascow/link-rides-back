from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
import adminactions.actions as actions
from main import models
from .filters.tmp_filter import TmpFilter 
from modeltranslation.admin import TranslationAdmin
from djangoql.admin import DjangoQLSearchMixin

@admin.register(models.TmpModel)
class TmpAdmin(TranslationAdmin, DjangoQLSearchMixin, ImportExportModelAdmin):
    list_display = ('name', 'image', 'description', 'role', 'version', )
    list_display_links = ('name', )
    list_filter = ('role', TmpFilter,)
    search_fields = ('name', 'description', )
    readonly_fields = ('version', )
    sortable_field_name = "name"
    fieldsets = (
        ('', {
            'fields': ('name', 'description', ),
        }),
        ("Image Inlines", {"classes": ("placeholder images-group",), "fields" : ('image', )}),
        ('FieldSetName2', { # видимый панель
            'classes': ('grp-collapse grp-open',), # grp-closed' - скрытый панель
            'fields' : ('role',),
        }),
    )


admin.site.site_header = "Django Admin"
admin.site.site_title = "Django Admin Portal"
admin.site.index_title = "Welcome to Django Admin Portal"
admin.site.site_url = "/admin/"

actions.add_to_site(admin.site)