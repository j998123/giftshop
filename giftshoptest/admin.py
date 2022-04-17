from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import Customer,Order,Product,Wishlist
import json
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['username','mobile','dateofbirth','address','emailaddress']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['Orderid','user_id','mobile','deliverdate','address','emailaddress']
    def has_add_permission(self, request):
        return False

class ProductAdmin(admin.ModelAdmin):
    list_display = ['Productid','Productname','Price','category','information','image']

class WishlistAdmin(admin.ModelAdmin):
    def prodlist(self,obj):
        return [pl.Productid for pl in obj.Productlist.all()]
    def user(self,obj):
        return obj.user_id.username
    prodlist.short_description = 'Productlist'
    list_display = ['listid','listname', 'user', 'deliverdate','prodlist']
    fieldsets = ((None,{'fields':('listid','listname', 'user_id', 'deliverdate','Productlist')}),)
    filter_horizontal = ('Productlist',)

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Wishlist,WishlistAdmin)

