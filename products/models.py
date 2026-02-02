from django.db import models
from django.contrib.auth.models import User

# For Category 
class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(max_length=255,blank=True)
    # category_img = models.ImageField(upload_to='categories/')

    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Yahan hum logic views se bhejenge
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.category_name
    
    
# Products

class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(max_length=500,blank=True)
    # price = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    # stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Yahan hum logic views se bhejenge
        super().save(*args, **kwargs)
    def __str__(self):
        return self.product_name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='variants')
    size = models.CharField(max_length=10,blank=True,null=True,default=None)
    color = models.CharField(max_length=20,blank=True,null=True,default=None)
    price = models.DecimalField(max_digits=10 ,decimal_places=2,default=0)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Yahan hum logic views se bhejenge
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.product.product_name} - {self.size or 'NA'} - {self.color or 'NA'}'
    
    
# Review
class Review(models.Model):
    RATING_CHOICES = [
        (1, '⭐ 1 Star'),
        (2, '⭐⭐ 2 Stars'),
        (3, '⭐⭐⭐ 3 Stars'),
        (4, '⭐⭐⭐⭐ 4 Stars'),
        (5, '⭐⭐⭐⭐⭐ 5 Stars'),
    ]
     
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product','user')    
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') # Ek user ek product ko do baar add na kar sake

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

