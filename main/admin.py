from django.contrib import admin
import adminactions.actions as actions
from django.contrib.auth.admin import UserAdmin
from main import models
from django.utils.html import format_html


@admin.register(models.UserModel)
class UserModelAdmin(UserAdmin):
    list_display = ('tg_id', 'show_im_taxi', 'phone_number', 'first_name', 'last_name', 'show_username_link', 'referrer', 'date_joined', 'updated_at', 'show_user_status')
    list_display_links = ('tg_id', )
    list_filter = ('date_joined', 'updated_at')
    search_fields = ('tg_id', 'first_name', 'last_name', )
    readonly_fields = ('date_joined', 'updated_at')
    fieldsets = (
        (None, {'fields': ('tg_id', 'password', 'first_name', 'last_name', 'username')}),
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
    list_display = ('passenger', 'taxi', 'need_tariff', 'from_latitude', 'from_longitude', 'to_latitude', 'to_longitude', 'show_price', 'created_at', 'updated_at', 'taxi_driving_at', 'finish_at')
    list_display_links = ('passenger', )
    list_filter = ('need_tariff', 'created_at', 'updated_at')
    search_fields = ('passenger__tg_id', 'taxi__user__tg_id')
    readonly_fields = ('created_at', 'updated_at')
    def show_price(self, obj: models.TaxiModel):
        return f"{obj.price} сум"
    show_price.short_description = "Цена"
    
@admin.register(models.TaxiInfoModel)
class TaxiInfoModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'latitude', 'longitude', 'status', 'tariff', 'car_brand', 'car_model', 'car_color', 'car_number', 'year', 'series_license', 'country_license', 'date_get_license', 'license_valid_until', 'photo_license', 'starting_at', 'latitude', 'longitude', 'status', 'created_at', 'updated_at')
    list_display_links = ('user', )
    list_filter = ('status', 'car_color', 'year', 'country_license', 'starting_at', 'created_at', 'updated_at')
    search_fields = ('user__tg_id', )
    readonly_fields = ('created_at', 'updated_at')
    
@admin.register(models.BallModel)
class BallModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'ball_type', 'count', 'description', 'created_at', 'updated_at', )
    list_display_links = ('user', )
    list_filter = ('ball_type', 'count', 'created_at', 'updated_at', )
    search_fields = ('user__tg_id', )
    
@admin.register(models.TariffModel)
class TariffModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'per_one_km', 'per_one_km_before', 'is_available')
    list_filter = ('is_available', )
@admin.register(models.TaxiConfirmationApplicationModel)
class TaxiConfirmationApplicationModelAdmin(admin.ModelAdmin):
    list_display = ('application', 'show_taxies',)

    def show_taxies(self, obj: models.TaxiConfirmationApplicationModel):
        return ', '.join([str(x) for x in obj.taxies.all()])


admin.site.site_header = "Link rides"
admin.site.site_title = "Link rides Portal"
admin.site.index_title = "Welcome to Link rides Portal"
admin.site.site_url = "/admin/"

actions.add_to_site(admin.site)
