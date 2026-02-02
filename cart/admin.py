from django.contrib import admin
from .models import Cart,CartItems

# Register your models here.
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('cart','variant','quantity')

admin.site.register(Cart)
admin.site.register(CartItems,CartItemsAdmin)