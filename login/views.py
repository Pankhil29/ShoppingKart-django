from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from order.models import Order
from .forms import SignupForm, LoginForm, UserUpdateForm
from django.contrib.auth import authenticate, login, logout
from cart.models import Cart, CartItems
from products.models import ProductVariant  


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user) # Pehle login karein
                merge_cart_after_login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
                
    return render(request, 'login/login.html', {'form': form})

def merge_cart_after_login(request, user):
    
    session_cart = request.session.get('cart', {})
    
    if session_cart:
        # 1. User ka Cart dhundo ya naya banao
        user_cart, created = Cart.objects.get_or_create(user=user)

        for variant_id, quantity in session_cart.items():
            try:
                # 2. Product ki jagah ProductVariant use karein (IMPORTANT FIX)
                variant = ProductVariant.objects.get(id=variant_id)
                
                # 3. Check karein ki ye variant pehle se DB cart mein hai ya nahi
                # Model field ka naam 'variant' hona chahiye 'product' nahi
                item, item_created = CartItems.objects.get_or_create(
                    cart=user_cart, 
                    variant=variant 
                )
                
                if not item_created:
                    item.quantity += int(quantity)
                else:
                    item.quantity = int(quantity)
                
                # Stock validation (Optional but safe)
                if item.quantity > variant.stock:
                    item.quantity = variant.stock
                    
                item.save()
            except (ProductVariant.DoesNotExist, ValueError):
                # Agar variant ID galat hai ya variant delete ho gaya hai
                continue
        
        # 4. Merge hone ke baad session cart ko saaf karein
        request.session['cart'] = {}
        request.session.modified = True

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
        else:
            messages.error(request, "Signup failed. Please check the details.")
    else:
        form = SignupForm()
    return render(request, 'login/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')


def Profile_view(request):
    return render(request, 'components/profile.html')

    
def Profile_view_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Aapka account update ho gaya hai!')
            return redirect('user_profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'components/profile_update.html', {'form': form})

def view_orders(request):
    orders = Order.objects.filter(user=request.user)\
        .prefetch_related(
            'items__product_variant__product'
        )\
        .order_by('-created_at')

    context = {
        'orders': orders,
    }
    
    return render(request, 'components/order_view.html', context)