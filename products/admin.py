from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
