from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
import adminactions.actions as actions
from django.contrib.auth.admin import UserAdmin
from main import models
from .filters.tmp_filter import TmpFilter 
from modeltranslation.admin import TranslationAdmin
from djangoql.admin import DjangoQLSearchMixin
from main import forms

@admin.register(models.UserModel)
class UserModelAdmin(admin.ModelAdmin):
    add_form = forms.UserModelCreationForm
    form = forms.UserModelChangeForm    
    list_display = ('tg_id', 'first_name', 'last_name', 'date_joined', 'updated_at', 'user_status', 'balance')
    list_display_links = ('tg_id', )
    list_filter = ('user_status',)
    search_fields = ('tg_id', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'updated_at', 'balance')
    fieldsets = (
        (None, {'fields': ('tg_id', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_status', 'balance')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    )      

@admin.register(models.DrivingModel)
class DrivingModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'starting_at', 'latitude', 'longitude', 'status')
    list_display_links = ('user', )
    list_filter = ('status',)
    search_fields = ('user__tg_id', 'latitude', 'longitude')
    readonly_fields = ('starting_at',)

@admin.register(models.TaxiModel)
class TaxiModelAdmin(admin.ModelAdmin):
    list_display = ('passenger', 'taxi', 'from_latitude', 'from_longitude', 'to_latitude', 'to_longitude', 'price', 'created_at', 'updated_at', 'taxi_driving_at', 'finish_at')
    list_display_links = ('passenger', )
    list_filter = ('price', 'created_at', 'updated_at')
    search_fields = ('passenger__tg_id', 'taxi__user__tg_id')
    readonly_fields = ('created_at', 'updated_at')

admin.site.site_header = "Django Admin"
admin.site.site_title = "Django Admin Portal"
admin.site.index_title = "Welcome to Django Admin Portal"
admin.site.site_url = "/admin/"

actions.add_to_site(admin.site)
