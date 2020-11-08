from django.db import models
from django.conf import settings

# Create your models here.
class Customer(models.Model):
    user_id = models.AutoField(primary_key=True)
    username= models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(default=None)

class File(models.Model):
    user_id = models.ForeignKey(Customer,to_field="user_id",on_delete=models.CASCADE)
    file_name = models.CharField(max_length=50)
    azur_file_name = models.CharField(primary_key=True,max_length=50)
    drive = models.CharField(max_length=50)
    directory = models.CharField(max_length=50)


