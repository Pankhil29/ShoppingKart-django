from django.contrib import admin
from .models import Category , Product, Review,ProductVariant, Wishlist

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name','slug')

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product','size','color','price','stock','is_active')

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name','category','is_available','updated_at')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user','product','rating')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductVariant,ProductVariantAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Wishlist)

