from django.urls import path
from . import views
from .dash_apps.finished_apps import SimpleExample

urlpatterns = [
    path('table/',views.table,name = 'table'),
    path('table/upload/', views.table_upload, name='table_upload'),
    path('charts/chartjs/',views.chartjs,name = 'chartjs'),

]
