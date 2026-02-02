from django.db import models
from django.contrib.auth.models import User
from products.models import ProductVariant,Product

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Cart'
    def __str__(self):
        return self.user.username
    
class CartItems(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    variant = models.ForeignKey(ProductVariant,null=True, blank=True,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = 'CartItems'
        
    def get_subtotal(self):
        return self.quantity * self.variant.price 
   
        