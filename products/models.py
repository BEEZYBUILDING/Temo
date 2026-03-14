from django.db import models
from django.utils.text import slugify
from users.models import CustomUser

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey('self', related_name='subcategories', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, related_name='products', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs): #override the default save functo and create your own
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs) #super calls the main save sunction and uses it to save the slug
        
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]
        
    def __str__(self):
        return self.name
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    sku = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    attributes = models.JSONField() # it allows  only the needed columns for each products so that there wont be unnesesarry columns
    is_active = models.BooleanField(default=True)
    
    class Meta:
        indexes = [ #allows you to filter abd search based on the field indexed
            models.Index(fields=['sku'])
        ]
    
    def __str__(self):
        return f"{self.product.name} - {self.sku}"
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.product} - {self.image_url}"
    