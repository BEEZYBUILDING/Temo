from django.db.models import Min
from rest_framework import serializers
from .models import Product, ProductVariant, ProductImage

class ProductVariantSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    in_stock = serializers.SerializerMethodField()
    
    def get_in_stock(self, obj):
        return obj.stock > 0
    
    class Meta:
        model = ProductVariant
        fields = [
            'product', 'sku', 'price', 'in_stock', 'attributes'
        ]
        
class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True) #for input
    input_variants = ProductVariantSerializer(many=True, write_only=True)
    # this is the variant eing nested in the product response thid means that when i return a product it will include all the variants automatically
    slug = serializers.SlugField(read_only=True)
    seller = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Product
        
        fields = [
            'id', 'name', 'slug', 'description',
            'category', 'seller', 'is_active', 
            'created_at', 'variants', 'input_variants'
        ]
        
    def create(self, validated_data):
        variants_data = validated_data.pop('input_variants') #creates a list with all the inout variants
        product = Product.objects.create(**validated_data) #it creates the an object called product
        
        for variant in variants_data:
            #it creates an object in the Productvariant that has the product and the variant
            ProductVariant.objects.create(product=product, **variant)
        return product   
    
class ProductImageSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = ProductImage
       
        fields = [
            'product', 'image_url', 'alt_text', 'order', 'is_primary'
        ]
        
class ProductListSerializer(serializers.ModelSerializer):
    
    min_price = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()
    
    def get_min_price(self, obj):
        result = obj.variants.aggregate(Min('price'))
        return result['price__min']
    
    def get_primary_image(self, obj):
        image = obj.images.filter(is_primary=True).first()
        return image.image_url if image else None
    
    def get_in_stock(self, obj):
        return obj.variants.filter(stock__gt=0).exists()
       
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category',
            'primary_image', 'min_price', 'in_stock'
        ]
        
class ProductDetailSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description',
            'category', 'seller', 'is_active', 
            'created_at', 'variants', 'images'
        ]