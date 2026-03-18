import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='category')
    is_active = django_filters.BooleanFilter(field_name='is_active')
    min_price = django_filters.NumberFilter(field_name='variants__price', lookup_expr='gte') 
    #variants__price goes through the variants relationship(it is the related name for products) and accesss the price section for the ProductVariant
    max_price = django_filters.NumberFilter(field_name='variants__price', lookup_expr='lte')
    in_stock = django_filters.NumberFilter(field_name='variants__stock', lookup_expr='gt')
    class Meta:
        model = Product
        fields = [
            'category', 'is_active', 'min_price', 'max_price', 'in_stock'
        ]
    