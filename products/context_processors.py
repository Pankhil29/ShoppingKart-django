from .models import Category,Product
from django.db.models import Avg
def category_list(req):
    category = Category.objects.all()
    return dict(category=category)



# def product_variant)




