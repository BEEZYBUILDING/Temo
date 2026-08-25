from orders.models import OrderItem

def check_verified_purchase(user, product):
    return OrderItem.objects.filter(
        order__user=user,
        order__status='COMPLETED',
        variant__product=product
    ).exists()
