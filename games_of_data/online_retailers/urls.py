from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('brand_comparision/', views.avg_price_by_ram, name="retailers")
    #path('test',views.test,name="test")
]
