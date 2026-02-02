from .models import CartItems
from products.models import Wishlist

def global_quantity(req):
    quantity = 0
    count = 0
    
    if req.user.is_authenticated:
        items = CartItems.objects.filter(cart__user=req.user)
        for item in items:
            quantity += item.quantity
        count = Wishlist.objects.filter(user=req.user).count()
    else: 
       
        cart = req.session.get('cart', {})
        if cart:
            for val in cart.values():
                try:
                    quantity += int(val)
                except ValueError:
                    continue
        
      
        wishlist = req.session.get('wishlist', [])
        count = len(wishlist)

   
    return {
        'cart_quantity': quantity,
        'wishlist_count': count
    }