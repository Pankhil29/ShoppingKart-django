from django.contrib import admin
from .models import Order,OrderItem

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','total_amount','status','updated_at')
    

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order','product_variant','quantity','price')

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)