from django.db import models
from products.models import Product
from users.models import CustomUser

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(CustomUser, related_name='reviews', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_review_per_user_product')
        ]
    
    def __str__(self):
        return f'{self.user}-{self.product}: {self.comment}, {self.rating}'