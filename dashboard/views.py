from django.shortcuts import get_object_or_404, render,redirect
from dashboard.forms import OrderStatusForm, ProductForm, ProductVariantForm,CategoryForm,UserAdminForm
from products.models import Product,ProductVariant,Category
from order.models import Order
from django.contrib.auth.models import User
from django.db.models import Min
from django.contrib import messages
from order.models import Order,OrderItem
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

# Sirf Staff aur Admin ke liye
staff_required = user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='login')

# Sirf Superuser (Admin) ke liye
admin_only = user_passes_test(lambda u: u.is_superuser, login_url='login')

@staff_required
def dashboard(req):
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_users = User.objects.count()
    
    context = {
        'total_orders': total_orders,
        'total_products': total_products,
        'total_users': total_users,
    }
    print(req.user)

    return render(req,'dashboard/dashboard.html',context)

def dashboard2(req):
    return render(req,'dashboard/dashboard-2.html')


# add Product
@staff_required
def product_list(req):
    query = req.GET.get('search')
    if query:
       product = Product.objects.filter(
            Q(product_name__icontains=query) | 
            Q(category__category_name__icontains=query)
        )
    else:
        product = Product.objects.all()
    
    context ={
        'products':product,
    }
    return render(req,'dashboard/products/product_list.html',context)

@staff_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) # Files image ke liye zaroori hai
        if form.is_valid():
            product = form.save(commit=False)
            product_name = form.cleaned_data['product_name']
            product.slug = slugify(product_name)
            product.updated_by = request.user 
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'dashboard/products/product_form.html', {'form': form, 'title': 'Add New Product'})

# 3. UPDATE
@staff_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product_name = form.cleaned_data['product_name']
            product.slug = slugify(product_name) 
            product.updated_by = request.user
            product.save()
            messages.success(request, "Product updated successfully!")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/products/product_form.html', {'form': form, 'title': 'Edit Product'})

# 4. DELETE
@staff_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    product.delete()
    messages.warning(request, "Product deleted!")
    return redirect('product_list')

# Product Variant
@staff_required
def variant_list(req):
    query = req.GET.get('search')
    if query:
        product = ProductVariant.objects.filter(
            Q(product__product_name__icontains=query) | 
            Q(color__icontains=query) |
            Q(price__icontains=query)
        )
    else:
        product = ProductVariant.objects.all()
    context = {
        'products':product,
    }
    return render(req,'dashboard/product_variant/variant_list.html',context)

@staff_required
def add_variant(request, product_id=None):
    # Agar kisi specific product ke liye variant add kar rahe hain
    initial_data = {}
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        initial_data['product'] = product

    if request.method == 'POST':
        form = ProductVariantForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False) 
            product.updated_by = request.user
            product.save()
            messages.success(request, "Variant added successfully!")
            return redirect('variant_list') # Ya variant list par bhejien
    else:
        form = ProductVariantForm(initial=initial_data)
    
    return render(request, 'dashboard/product_variant/variant_form.html', {'form': form})

@staff_required
def variant_update(request, pk):
    product = get_object_or_404(ProductVariant, pk=pk)
    if request.method == 'POST':
        form = ProductVariantForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False) 
            product.updated_by = request.user
            product.save()
            messages.success(request, "Product updated successfully!")
            return redirect('variant_list')
    else:
        form = ProductVariantForm(instance=product)
    return render(request, 'dashboard/product_variant/variant_form.html', {'form': form, 'title': 'Edit Product'})

@staff_required
def variant_delete(request, pk):
    product = get_object_or_404(ProductVariant, pk=pk)
    product.delete()
    messages.warning(request, "Product deleted!")
    return redirect('variant_list')


# Category
@staff_required
def category_list(req):
    query = req.GET.get('search')
    if query:
        category = Category.objects.filter(
            Q(category_name__icontains=query) | 
            Q(description__icontains=query) 
        )
    else:
        category = Category.objects.all()
    context = {
        'category':category
    }
    return render(req,'dashboard/category/category_list.html',context)

@staff_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category_name = form.cleaned_data['category_name']
            category.slug = slugify(category_name) 
            category.save()
            messages.success(request, "Product added successfully!")
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category/category_form.html', {'form': form, 'title': 'Add New Category'})

@staff_required
def category_update(request,pk):
    category = get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category) # Files image ke liye zaroori hai
        if form.is_valid():
            category = form.save(commit=False)
            category_name = form.cleaned_data['category_name']
            category.slug = slugify(category_name) 
            category.save()
            messages.success(request, "Product updated successfully!")
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/category/category_form.html', {'form': form, 'title': 'updated Category'})

@staff_required
def category_delete(req,pk):
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    return redirect('category_list')

# User
@admin_only
def user_list(req):
    query = req.GET.get('search')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(email__icontains=query) |
            Q(first_name__icontains=query)
        )
    else:
        users = User.objects.all()
    context = {
        'users':users
    }
    return render(req,'dashboard/user/user_list.html',context)

# def add_user(req):
    if req.method == 'POST':
        form = UserAdminForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserAdminForm()
    context = {
        'form' : form
    }
    return render(req,'dashboard/user/user_form.html',context)
@admin_only
def user_update(req,pk):
    users = get_object_or_404(User,pk=pk)
    if req.method == 'POST':
        form = UserAdminForm(req.POST,instance=users)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserAdminForm(instance=users)
    context = {
        'form':form,
    }
    return render(req,'dashboard/user/user_form.html',context)

@admin_only
def user_deactivate(request, pk):
    users = get_object_or_404(User, pk=pk)
    users.is_active = not users.is_active
    users.save()
    status = "activated" if users.is_active else "deactivated"
    messages.info(request, f"User {users.username} has been {status}.")
    return redirect('user_list')


# Order 
@staff_required
def order_list(request):
    query = request.GET.get('search')
    if query:
        # Order ID ya Order Number se search
        orders = Order.objects.filter(
            Q(id__icontains=query) | 
            Q(phone__icontains=query) |
            Q(user__username__icontains=query) # Customer name se bhi
        )
    else:
        orders = Order.objects.all()
    return render(request, 'dashboard/order/order_list.html', {'orders': orders})

@staff_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order) # Order ke saare products
    print(order_items)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False) 
            order.updated_by = request.user
            order.save()
            messages.success(request, f"Order #{order.id} status updated!")
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderStatusForm(instance=order)

    context = {
        'order': order,
        'order_items': order_items,
        'form': form
    }
    return render(request, 'dashboard/order/order_detail.html', context)