from django.urls import path
from . import views
from .dash_apps.finished_apps import SimpleExample

urlpatterns = [
    path('login/',views.login,name = 'login'),
    path('signup/',views.signup, name = 'signup'),
    path('register/',views.register,name='register'),
    path('auth_user/',views.auth_user,name="authuser"),
    path('logout/',views.logout,name = 'logout'),
    path('table/',views.table,name = 'table'),
    path('table/upload/', views.table_upload, name='table_upload'),
    path('table/show/',views.show_table,name = "show_table"),
    path('charts/chartjs/',views.chartjs,name = 'chartjs'),

]
