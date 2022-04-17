from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import JSONField
# Create your models here.


class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True,max_length=45,blank=True,null=True)
    password = models.CharField(max_length=45,blank=True,null=True)
    mobile = PhoneNumberField()
    dateofbirth = models.DateField(null=True)
    address = models.CharField(max_length=255,blank=True,null=True)
    emailaddress = models.CharField(max_length=255, blank=True, null=True)


class Product(models.Model):
    Productid = models.IntegerField(primary_key=True)
    Productname = models.CharField(unique=True,max_length=45,blank=True,null=True)
    Price = models.IntegerField()
    category = models.CharField(max_length=255, blank=True, null=True)
    information = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(max_length=1000,blank=True,null=True)


class Order(models.Model):
    ORDER_STATUS_ENUM = {
        "UNPAID": 1,
        "UNSEND": 2,
        "UNRECRIVED": 3,
        "FINISH": 4,
    }
    ORDER_STATUS_CHOICES = (
        (1,"Pending Payment"),
        (2, "Pending Shipment"),
        (3, "Awaiting confirmation of receipt"),
        (4, "Completed"),
        (5, "Cancelled"),
    )
    Orderid = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    Price = models.IntegerField(null=True)
    mobile = PhoneNumberField()
    deliverdate = models.DateField(null=True)
    address = models.CharField(max_length=255,blank=True,null=True)
    emailaddress = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES,default=1)
    Productlist = models.ManyToManyField(Product)

class Wishlist(models.Model):
   listid = models.IntegerField(primary_key=True)
   listname = models.CharField(unique=True, max_length=45, blank=True, null=True)
   user_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
   deliverdate = models.DateField(null=True)
   address = models.CharField(max_length=255, blank=True, null=True)
   emailaddress = models.CharField(max_length=255, blank=True, null=True)
   Productlist = models.ManyToManyField(Product)


