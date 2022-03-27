# Generated by Django 4.0.3 on 2022-03-20 03:41

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('giftshoptest', '0006_delete_customerinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='customerInfo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=45, null=True, unique=True)),
                ('password', models.CharField(blank=True, max_length=45, null=True)),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('dateofbirth', models.DateField(null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
