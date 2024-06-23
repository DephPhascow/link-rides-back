from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
import adminactions.actions as actions
from main import models
from .filters.tmp_filter import TmpFilter 
from modeltranslation.admin import TranslationAdmin
from djangoql.admin import DjangoQLSearchMixin

@admin.register(models.UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'tg_id', 'first_name', 'last_name', 'join_at', 'updated_at', 'status', 'balance')
    list_display_links = ('username', )
    list_filter = ('status',)
    search_fields = ('username', 'tg_id', 'first_name', 'last_name')
    readonly_fields = ('join_at', 'updated_at', 'balance')

@admin.register(models.DrivingModel)
class DrivingModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'starting_at', 'latitude', 'longitude', 'status')
    list_display_links = ('user', )
    list_filter = ('status',)
    search_fields = ('user__username', 'latitude', 'longitude')
    readonly_fields = ('starting_at',)

@admin.register(models.TaxiModel)
class TaxiModelAdmin(admin.ModelAdmin):
    list_display = ('passenger', 'taxi', 'from_latitude', 'from_longitude', 'to_latitude', 'to_longitude', 'price', 'created_at', 'updated_at', 'taxi_driving_at', 'finish_at')
    list_display_links = ('passenger', )
    list_filter = ('price', 'created_at', 'updated_at')
    search_fields = ('passenger__username', 'taxi__user__username')
    readonly_fields = ('created_at', 'updated_at')

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
        ('FieldSetName2', {
            'classes': ('grp-collapse grp-open',),
            'fields' : ('role',),
        }),
    )

admin.site.site_header = "Django Admin"
admin.site.site_title = "Django Admin Portal"
admin.site.index_title = "Welcome to Django Admin Portal"
admin.site.site_url = "/admin/"

actions.add_to_site(admin.site)
