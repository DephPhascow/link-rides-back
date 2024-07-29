from django.contrib import admin
import adminactions.actions as actions
from django.contrib.auth.admin import UserAdmin
from main import models
from django.utils.html import format_html


@admin.register(models.UserModel)
class UserModelAdmin(UserAdmin):
    list_display = ('tg_id', 'show_im_taxi', 'first_name', 'last_name', 'show_username_link', 'date_joined', 'updated_at', 'show_user_status')
    list_display_links = ('tg_id', )
    list_filter = ('date_joined', 'updated_at')
    search_fields = ('tg_id', 'first_name', 'last_name', )
    readonly_fields = ('first_name', 'last_name', 'username', 'date_joined', 'updated_at')
    fieldsets = (
        (None, {'fields': ('tg_id', 'password', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("tg_id", "password1", "password2"),
            },
        ),
    )    
    def show_username_link(self, obj: models.UserModel):
        if not obj.username:
            return '-'
        return format_html(f"<a href='https://t.me/{obj.username}'>{obj.username}</a>")
    
    def show_im_taxi(self, obj: models.UserModel):
        return 'Да' if obj.get_taxi_infos else 'Нет'
    
    def show_user_status(self, obj: models.UserModel):
        return obj.user_status

    show_username_link.short_description = "TG username"
    show_im_taxi.short_description = "Является таксистом"
    show_user_status.short_description = "Статус пользователя"

@admin.register(models.TaxiModel)
class TaxiModelAdmin(admin.ModelAdmin):
    list_display = ('passenger', 'taxi', 'from_latitude', 'from_longitude', 'to_latitude', 'to_longitude', 'price', 'created_at', 'updated_at', 'taxi_driving_at', 'finish_at')
    list_display_links = ('passenger', )
    list_filter = ('price', 'created_at', 'updated_at')
    search_fields = ('passenger__tg_id', 'taxi__user__tg_id')
    readonly_fields = ('created_at', 'updated_at')
    
@admin.register(models.TaxiInfoModel)
class TaxiInfoModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'car_brand', 'car_model', 'car_color', 'car_number', 'year', 'series_license', 'country_license', 'date_get_license', 'license_valid_until', 'photo_license', 'starting_at', 'latitude', 'longitude', 'status', 'created_at', 'updated_at')
    list_display_links = ('user', )
    list_filter = ('status', 'car_color', 'year', 'country_license', 'starting_at', 'created_at', 'updated_at')
    search_fields = ('user__tg_id', )
    readonly_fields = ('created_at', 'updated_at')


admin.site.site_header = "Django Admin"
admin.site.site_title = "Django Admin Portal"
admin.site.index_title = "Welcome to Django Admin Portal"
admin.site.site_url = "/admin/"

actions.add_to_site(admin.site)
