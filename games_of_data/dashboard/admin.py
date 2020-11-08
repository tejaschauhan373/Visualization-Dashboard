from django.contrib import admin
from .models import Customer,File
# Register your models here.

@admin.register(Customer)
class DashboardAdmin(admin.ModelAdmin):
    list_display =("user_id","username","password","first_name","last_name","email")

@admin.register(File)
class DashboardAdmin(admin.ModelAdmin):
    list_display =("user_id","file_name","azur_file_name","drive","directory")