
from django.shortcuts import render
from products.models import Product,ProductVariant
from django.db.models import Q
from django.db.models import Min,Avg

def home(req):
    products = (Product.objects.filter(is_available=True).annotate(avg_rating=Avg('reviews__rating'),min_price=Min('variants__price')))
    print(products)
    products = products.filter(min_price__isnull=False)
    # variant = Product.objects.get(id=product.id)
    for p in products:
        p.avg_rating = round(p.avg_rating, 1) if p.avg_rating else 0
    context ={
        'products' : products,
        # 'variants':variant,
    }
    return render(req,'home.html',context)
  


def search(req):
    keyword = req.GET.get('keyword')
    product = None
    
    if keyword:
        # 1. Annotate karke min_price nikalo
        # 2. Phir filter lagao keyword aur availability par
        product = Product.objects.annotate(
            min_price=Min('variants__price')
        ).filter(
            Q(product_name__icontains=keyword) | 
            Q(description__icontains=keyword),
            is_available=True
        )
    
    context = {
        'products': product, 
        'keyword': keyword
    }
    return render(req, 'search.html', context)