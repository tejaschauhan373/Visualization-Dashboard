# Generated by Django 3.1.1 on 2020-11-08 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_customer_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=50)),
                ('azur_file_name', models.CharField(max_length=50)),
                ('drive', models.CharField(max_length=50)),
                ('directory', models.CharField(max_length=50)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.customer')),
            ],
        ),
    ]