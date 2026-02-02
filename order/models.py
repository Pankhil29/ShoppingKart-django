from django.db import models
from django.contrib.auth.models import User
from products.models import ProductVariant

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PLACED', 'Placed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    
    # Shipping Info
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    
    # Payment Info
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # Important: Link to Variant
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    
    # Snapshot fields (Agar future me price badal gayi, to order history me purani price dikhni chahiye)
    product_name = models.CharField(max_length=200) 
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at time of purchase

    def get_total(self):
        return self.quantity * self.price
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"