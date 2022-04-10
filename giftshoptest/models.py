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



class Order(models.Model):
    Orderid = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True,max_length=45,blank=True,null=True)
    mobile = PhoneNumberField()
    deliverdate = models.DateField(null=True)
    address = models.CharField(max_length=255,blank=True,null=True)
    emailaddress = models.CharField(max_length=255, blank=True, null=True)
    Productlist = models.JSONField(null=True)

class Product(models.Model):
    Productid = models.IntegerField(primary_key=True)
    Productname = models.CharField(unique=True,max_length=45,blank=True,null=True)
    Price = models.IntegerField()
    category = models.CharField(max_length=255, blank=True, null=True)
    information = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(max_length=1000,blank=True,null=True)

class Wishlist(models.Model):
   listnumber = models.IntegerField(primary_key=True)
   listname = models.CharField(unique=True, max_length=45, blank=True, null=True)
   username = models.CharField(unique=True,max_length=45,blank=True,null=True)
   category = models.CharField(max_length=255, blank=True, null=True)
   deliverdate = models.DateField(null=True)
   Productlist = models.JSONField()


