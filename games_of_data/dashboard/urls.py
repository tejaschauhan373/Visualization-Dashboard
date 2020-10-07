from django.urls import path
from . import views
from .dash_apps.finished_apps import SimpleExample

urlpatterns = [
    path('home/', views.home, name='home'),
]
