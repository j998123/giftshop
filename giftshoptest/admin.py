from django.contrib import admin
from .models import Customer,Order,Product
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['username','mobile','dateofbirth','address','emailaddress']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['Orderid','username','mobile','deliverdate','address','emailaddress','Productlist']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['Productid','Productname','Price','category','information','image']

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Product,ProductAdmin)
