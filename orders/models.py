from django.db import models, transaction
from products.models import ProductVariant
from users.models import CustomUser

# Create your models here.
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        PROCESSING = "PROCESSING", "Processing"
        SHIPPED = "SHIPPED", "Shipped"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"
        REFUNDED = "REFUNDED", "Refunded"
        COMPLETED = 'COMPLETED', 'Completed'
    
    VALID_TRANSITIONS = {
        'PENDING': ['CONFIRMED', 'CANCELLED'],
        'CONFIRMED': ['PROCESSING', 'CANCELLED'],
        'PROCESSING': ['SHIPPED','CANCELLED'],
        'SHIPPED': ['DELIVERED'],
        'DELIVERED': ['COMPLETED', 'REFUNDED'],
        'COMPLETED': [],
        'CANCELLED': [],
        'REFUNDED': []
    }

    def transition_to(self, new_status):
        if new_status not in self.VALID_TRANSITIONS.get(self.status, []):
            raise ValueError(f'Cannot transition from {self.status} to {new_status}')
        self.status = new_status
        self.save()
    
    user = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE)
    address = models.JSONField()
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey(Coupon, related_name='coupon', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, related_name='item_variant', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    variant_attributes = models.JSONField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id} - {self.order}"
    

class Coupon(models.Model):
    class Discount(models.TextChoices):
        FLAT = 'FLAT', 'Flat'
        PERCENTAGE = 'PERCENTAGE', 'Percentage'
    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(max_length=10, choices=Discount.choices)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order_value = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    expiry_date = models.DateTimeField()
    max_uses = models.IntegerField(default=0)
    current_uses = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def is_valid(self, order_value):
        if timezone.now() >= self.expiry_date:
            raise ValueError(f'This coupon has expired')
        if not self.is_active:
            raise ValueError(f'Coupon is no longer active')
        if self.current_uses >= self.max_uses:
            raise ValueError(f'Coupon has reached the maximum number of uses')
        if order_value < self.minimum_order_value:
            raise ValueError(f'Minimum amount is {self.minimum_order_value}')
        
        return True

    @staticmethod
    def apply(code, order_value):
        with transaction.atomic():
            coupon = Coupon.objects.select_for_update().get(code=code)
            coupon.is_valid(order_value)
            coupon.current_uses += 1
            coupon.save()
            return coupon

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Coupon {self.discount_value}"


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, related_name='history', on_delete=models.CASCADE)
    previous_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order}, {self.previous_status}-{self.new_status}"