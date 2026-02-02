from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ReviewForm
from .models import Category, Product, ProductVariant, Review, Wishlist
from django.db.models import Avg, Min, FloatField, Q , Count
from django.db.models.functions import Cast
import json


def category_page(request, cat_id):
    category = get_object_or_404(Category, pk=cat_id)
  
    products = Product.objects.filter(category=category, is_available=True).annotate(
        min_price=Min('variants__price')
    )
    products = products.filter(min_price__isnull=False)
    context = {
        'category_products': products,
        'single_category': category,
    }
    return render(request, 'products/category_page.html', context)

def product_list(request):
    # Optimization 1: select_related se category ek hi query mein aa jayegi
    products = Product.objects.filter(is_available=True).select_related('category').annotate(
        avg_rating=Avg('reviews__rating'),
        min_price=Min('variants__price')
    ).filter(min_price__isnull=False)
    
    # --- Filtering Logic (Cleaner) ---
    category_id = request.GET.get('category')
    min_p = request.GET.get('min_price')
    max_p = request.GET.get('max_price')
    rating_val = request.GET.get('rating')

    if category_id:
        products = products.filter(category_id=category_id)
    if min_p:
        products = products.filter(min_price__gte=min_p)
    if max_p:
        products = products.filter(min_price__lte=max_p)
    
    # Validation for float conversion
    if rating_val:
        try:
            products = products.filter(avg_rating__gte=float(rating_val))
        except ValueError:
            pass 

    categories = Category.objects.all()
    
    # Optimization 2: Rounding template mein karein ya aggregate mein, looping avoid karein
    context = {
        'products': products.distinct(),
        'category': categories,
        'min_price': min_p,
        'max_price': max_p,
        'rating': rating_val,
        'selected_category': int(category_id) if (category_id and category_id.isdigit()) else None,
    }
    return render(request, 'products/product.html', context)

def product_details_page(request, slug):
    # 1. Product Fetching
    product = get_object_or_404(Product, slug=slug, is_available=True)
    
    # 2. Optimized Variants Query
    active_variants = product.variants.filter(is_active=True)
    stats = active_variants.aggregate(min_price=Min('price'))
    product.min_price = float(stats['min_price']) if stats['min_price'] is not None else 0.0

    # 3. Redundancy Removal
    has_size = any(v.size for v in active_variants)
    has_color = any(v.color for v in active_variants)

    # 4. Wishlist Logic
    user_wishlist = False
    if request.user.is_authenticated:
        user_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    else:
        session_wishlist = request.session.get('wishlist', [])
        user_wishlist = str(product.id) in [str(id) for id in session_wishlist]

    # 5. Reviews & Ratings Logic (UPDATED FOR BAR GRAPHS)
    reviews = product.reviews.select_related('user').all().order_by('-updated_at')
    total_reviews = reviews.count()
    
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    avg_rating = round(float(avg_rating), 1)

    # Individual Rating Counts (Excellent, Very Good, etc.)
    # Hum ek hi query mein saare counts nikaal rahe hain optimize karne ke liye
    rating_stats = reviews.aggregate(
        r5=Count('id', filter=Q(rating=5)),
        r4=Count('id', filter=Q(rating=4)),
        r3=Count('id', filter=Q(rating=3)),
        r2=Count('id', filter=Q(rating=2)),
        r1=Count('id', filter=Q(rating=1)),
    )

    # Percentages nikalna taaki progress bar ki width set ho sake
    def get_pct(val):
        if total_reviews > 0:
            return (val / total_reviews) * 100
        return 0

    rating_breakdown = [
        {'label': 'Excellent', 'count': rating_stats['r5'], 'pct': get_pct(rating_stats['r5']), 'color': '#038d63'},
        {'label': 'Very Good', 'count': rating_stats['r4'], 'pct': get_pct(rating_stats['r4']), 'color': '#038d63'},
        {'label': 'Good',      'count': rating_stats['r3'], 'pct': get_pct(rating_stats['r3']), 'color': '#f5a623'},
        {'label': 'Average',   'count': rating_stats['r2'], 'pct': get_pct(rating_stats['r2']), 'color': '#ffb400'},
        {'label': 'Poor',      'count': rating_stats['r1'], 'pct': get_pct(rating_stats['r1']), 'color': '#ff3f6c'},
    ]

    # 6. Variant Data for JS
    variant_data = [
        {
            "id": v.id,
            "size": v.size or "",
            "color": v.color or "",
            "price": str(v.price),
            "stock": v.stock
        }
        for v in active_variants
    ]

    # 7. POST Logic
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={
                    'rating': form.cleaned_data['rating'], 
                    'comment': form.cleaned_data['comment']
                }
            )
            return redirect('product_details_page', slug=slug)
    else:
        form = ReviewForm()
    
    context = {
        'product': product,
        'variants': active_variants,
        'has_size': has_size,
        'has_color': has_color,
        'user_wishlist': user_wishlist,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'rating_breakdown': rating_breakdown, # Naya data for bar graphs
        'total_reviews': total_reviews,
        'form': form,
        'variant_data': json.dumps(variant_data), 
    }
    return render(request, 'products/product_details.html', context)



def wishlist_page(request): # Naam change kiya taaki confusion na ho
    product_id = request.GET.get('id')
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if not created:
            wishlist_item.delete()
            status = "removed"
        else:
            status = "added"
        # Logged-in user ka total count nikalo
        count = Wishlist.objects.filter(user=request.user).count()
    else:
        wishlist = request.session.get('wishlist', [])
        if str(product_id) in wishlist:
            wishlist.remove(str(product_id))
            status = "removed"
        else:
            wishlist.append(str(product_id))
            status = "added"
        request.session['wishlist'] = wishlist
        request.session.modified = True
        count = len(wishlist)
        
    return JsonResponse({'status': status, 'wishlist_count': count})

def wishlist_view(request):
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

    context = {
        'products': products,
    }
    return render(request, 'products/wishlist.html', context)