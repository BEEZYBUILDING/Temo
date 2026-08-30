from rest_framework import serializers
from .models import Coupon, Order, OrderItem, OrderStatusHistory

class CheckoutSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    coupon_code = serializers.CharField(required=False, allow_blank=True)

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'status', 'user', 'total', 'created_at'
        ]    

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields =  [
            'variant', 'product_name', 'quantity', 
            'unit_price', 'line_total'
        ]

class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = [
            'previous_status', 'new_status', 'created_by', 'note',
            'changed_by'
        ]

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    history = OrderStatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'address', 'status', 'subtotal', 'shipping_cost',  
            'tax_amount', 'discount_amount','total', 'created_at', 
            'updated_at', 'items', 'history'
        ]

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            'code', 'discount_type', 'discount_value', 'minimum_order_value',
            'expiry_date', 'max_uses', 'is_active'
        ]
    
    def validate(self, data):
        if data['discount_type'] == 'PERCENTAGE' and data['discount_value'] > 100:
            raise serializers.ValidationError('Percentage discount cannot exceed 100%')
        return data
