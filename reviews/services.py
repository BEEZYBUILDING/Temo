from django.db.models import Avg, Count
from orders.models import OrderItem
from products.models import Product
from .models import Review

def check_verified_purchase(user, product):
    return OrderItem.objects.filter(
        order__user=user,
        order__status='COMPLETED',
        variant__product=product
    ).exists()

def update_product_rating(product_id):
    result = Review.objects.filter(product_id=product_id).aggregate(Avg('rating'), Count('id'))
    product = Product.objects.get(id=product_id)
    product.average_rating = result['rating__avg'] or 0
    product.review_count = result['id__count']
    product.save()