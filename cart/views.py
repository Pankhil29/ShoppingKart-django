from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, ProductVariant, Wishlist
from cart.models import Cart, CartItems
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.functions import Cast
from django.db.models import Avg, Min, FloatField, Q , Count

def _cart_id(request):
    """ Helper to get session key """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request):
    if request.method == 'POST':
        variant_id = request.POST.get('variant_id')
        print(variant_id)
        # 1. Validation: variant_id hai ya nahi
        if not variant_id:
            messages.error(request, "Please select a variant/size.")
            return redirect(request.META.get('HTTP_REFERER', 'product'))

        variant = get_object_or_404(ProductVariant, id=variant_id)
        
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1

        # 2. Stock Check
        if variant.stock <= 0:
            messages.warning(request, "Product is out of stock.")
            return redirect(request.META.get('HTTP_REFERER', 'product'))

      
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            # Yahan model name check kar lena (CartItem ya CartItems)
            cart_item, created = CartItems.objects.get_or_create(cart=cart, variant=variant)
            
            if not created:
                new_qty = cart_item.quantity + quantity
            else:
                new_qty = quantity

            if new_qty <= variant.stock:
                cart_item.quantity = new_qty
                cart_item.save()
                # messages.success(request, "Added to cart!")
            else:
                cart_item.quantity = variant.stock
                cart_item.save()
                # messages.warning(request, f"Only {variant.stock} units available. Stock limit reached.")

       
        else:
            cart = request.session.get('cart', {})
            key = str(variant_id)
            current_qty = cart.get(key, 0)
            new_qty = current_qty + quantity
            
            if new_qty <= variant.stock:
                cart[key] = new_qty
                # messages.success(request, "Added to temporary cart (Login to save).")
            else:
                cart[key] = variant.stock
                # messages.warning(request, "Stock limit reached.")
            
            request.session['cart'] = cart
            request.session.modified = True # Session update confirm karne ke liye

    return redirect('cart_detail')

def cart_detail(request):
    cart_items_data = []
    total = 0
    total_quantity = 0

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            db_items = CartItems.objects.filter(cart=cart, is_active=True)
            for item in db_items:
                subtotal = item.variant.price * item.quantity
                total += subtotal
                total_quantity += item.quantity
                cart_items_data.append({
                    'variant': item.variant,
                    'quantity': item.quantity,
                    'subtotal': subtotal,
                    'product': item.variant.product # Access parent product
                })
        except Cart.DoesNotExist:
            pass # Empty cart
    else:
        # Guest Cart
        cart = request.session.get('cart', {})
        for variant_id, qty in cart.items():
            try:
                variant = ProductVariant.objects.get(id=variant_id)
                subtotal = variant.price * qty
                total += subtotal
                total_quantity += qty
                cart_items_data.append({
                    'variant': variant,
                    'quantity': qty,
                    'subtotal': subtotal,
                    'product': variant.product
                })
            except ProductVariant.DoesNotExist:
                continue

    discount = (total *10)/100 # Logic baad me daalna
    final_total = total - discount
    if request.user.is_authenticated:
        # User ki wishlist fetch karo aur har product ka minimum price nikaalo
        wishlist_qs = Wishlist.objects.filter(user=request.user).select_related('product').annotate(
            min_price=Cast(Min('product__variants__price'), FloatField())
        )
        products = [item.product for item in wishlist_qs]
        # Hamne annotate product par kiya tha, toh min_price wahan se milega
        for p, item in zip(products, wishlist_qs):
            p.min_price = item.min_price
    else:
        # Guest user ke liye session se IDs lo
        session_wishlist = request.session.get('wishlist', [])
        products = Product.objects.filter(id__in=session_wishlist, is_available=True).annotate(
            min_price=Cast(Min('variants__price'), FloatField())
        )
    print(products)
    context = {
        'cart_items': cart_items_data,
        'total': total,
        'discount':discount,
        'final_total': final_total,
        'total_quantity': total_quantity,
        'wishlist_product': products,
    }
    return render(request, 'products/cart.html', context)

# --- Action Views (Simplified) ---

def increase_quantity(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    
    if request.user.is_authenticated:
        cart_item = CartItems.objects.get(cart__user=request.user, variant=variant)
        if cart_item.quantity < variant.stock:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart = request.session.get('cart', {})
        key = str(variant_id)
        if key in cart and cart[key] < variant.stock:
            cart[key] += 1
            request.session['cart'] = cart
    
    return redirect('cart_detail')

def decrease_quantity(request, variant_id):
    if request.user.is_authenticated:
        cart_item = CartItems.objects.get(cart__user=request.user, variant_id=variant_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    else:
        cart = request.session.get('cart', {})
        key = str(variant_id)
        if key in cart:
            if cart[key] > 1:
                cart[key] -= 1
            else:
                del cart[key]
            request.session['cart'] = cart
            
    return redirect('cart_detail')

def remove_from_cart(request, variant_id):
    if request.user.is_authenticated:
        CartItems.objects.filter(cart__user=request.user, variant_id=variant_id).delete()
    else:
        cart = request.session.get('cart', {})
        key = str(variant_id)
        if key in cart:
            del cart[key]
            request.session['cart'] = cart
            
    return redirect('cart_detail')

