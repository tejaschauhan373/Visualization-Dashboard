from django.contrib import admin
from .models import Customer, File, SignUpVerification


# Register your models here.

@admin.register(Customer)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "password", "first_name", "last_name", "email", "forgot_pwd_timestamp",
                    "profile_photo_uploaded")


@admin.register(File)
class DashboardAdmin(admin.ModelAdmin):
    list_display = (
    "user_id", "file_name", "azur_file_name", "azur_file_share", "azur_container", "file_type", "file_size")


@admin.register(SignUpVerification)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ("username", "password", "first_name", "last_name", "email", "signup_timestamp")
