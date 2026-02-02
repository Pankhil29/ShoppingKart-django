from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction # Very Important for orders
from cart.models import Cart
from .models import Order, OrderItem

@login_required(login_url='login')
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.select_related('variant').all()
    except Cart.DoesNotExist:
        return redirect('product') # Agar cart khali hai to wapas bhejo

    if not cart_items.exists():
        return redirect('product')

    # Calculation
    total = sum(item.get_subtotal() for item in cart_items)
    discount = (total * 10) / 100 
    grand_total = total - discount
    
    if request.method == 'POST':
        # ATOMIC TRANSACTION: Sab kuch sahi hoga tabhi DB me save hoga
        try:
            with transaction.atomic():
                # 1. Create Order
                order = Order.objects.create(
                    user=request.user,
                    name=request.POST['name'],
                    phone=request.POST['phone'],
                    address=request.POST['address'],
                    city=request.POST['city'],
                    state=request.POST['state'],
                    pincode=request.POST['pincode'],
                    total_amount=grand_total,
                    status='PLACED'
                )

                # 2. Move Cart Items to Order Items & DEDUCT STOCK
                for item in cart_items:
                    variant = item.variant
                    
                    # Stock Check (Very Important)
                    if variant.stock < item.quantity:
                        raise Exception(f"Sorry! {variant.product.product_name} is out of stock.")

                    # Create Order Item
                    OrderItem.objects.create(
                        order=order,
                        product_variant=variant,
                        product_name=variant.product.product_name, # Snapshot name
                        price=variant.price, # Snapshot price
                        quantity=item.quantity
                    )

                    # Deduct Stock
                    variant.stock -= item.quantity
                    variant.save()

                # 3. Clear Cart
                cart_items.delete() # Items delete karo
                # cart.delete() # Optional: Pura cart uda dena hai to ye use karo

                return redirect('order_success', order_id=order.id)
                
        except Exception as e:
            # Agar stock kam hai ya koi error aayi, to wapas checkout pe bhej do error ke sath
            messages.error(request, str(e))
            return redirect('checkout')

    context = {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'grand_total': grand_total,
    }
    return render(request, 'order/checkout.html', context)

@login_required(login_url='login')
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # Order items dikhane ke liye
    order_items = order.items.all()
    total = sum(item.get_total() for item in order_items)
    discount = (total * 10) / 100 
    grand_total = total - discount
    
    context = {
        'order': order,
        'order_items': order_items,
        'total': total,
        'grand_total' : grand_total
    }
    return render(request, 'order/success.html', context)