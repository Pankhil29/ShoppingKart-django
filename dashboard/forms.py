from django import forms
from products.models import Product,ProductVariant,Category
from django.contrib.auth.models import User
from order.models import Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product 
        fields = ['product_name','category', 'description', 'image', 'is_available']

        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter slug'}),
            'category': forms.Select(attrs={'class': 'form-control select2'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'custom-file-input'}),
        }
        
class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['product', 'size', 'color', 'price', 'stock', 'is_active']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control select2'}),
            'size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. XL, 10, 42'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Red, Blue'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','description']
        widgets = {
            'category_name' :forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. Clothes,Electronics'}),
            'description': forms.TextInput(attrs={'class':'form-control','placeholder':'Write Description...'}),
        }

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','is_staff','is_active'] 
        widgets = {
            'username' :forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form_control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user','status'] # 'is_ordered' payment confirm karne ke liye
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }