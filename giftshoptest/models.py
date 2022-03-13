from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class customerInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True,max_length=45,blank=True,null=True)
    password = models.CharField(max_length=45,blank=True,null=True)
    mobile = PhoneNumberField()
    dateofbirth = models.DateField(null=True)
    address = models.CharField(max_length=255,blank=True,null=True)


# class Category(models.Model):
#     name = models.CharField(max_length=255,db_index=True)
#     slug = models.SlugField(max_length=255,unique=True)
#
#     class Meta:
#         verbose_name_plural = 'categories'
#
#     def __str__(self):
#         return self.name
#
# class Product(models.Model):
#     categpry = models.ForeignKey(Category,related_name='prpduct',on_delete=models.CASCADE)