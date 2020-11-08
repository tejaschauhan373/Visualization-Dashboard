from django.urls import path
from . import views

urlpatterns = [
    path('finance/', views.finance, name='finance'),
]
