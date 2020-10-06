from django.urls import path
from . import views
from .dash_apps.finished_apps import simple

urlpatterns = [
    path('home/', views.home, name='home'),
]
