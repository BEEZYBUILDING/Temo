from rest_framework import serializers
from .models import Product, ProductVariant, ProductImage

class ProductVariantSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = [
            'product', 'sku', 'price', 'stock', 'attributes'
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