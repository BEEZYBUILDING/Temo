from redis_client import redis_client
from products.models import ProductVariant

class CartService:
    
    @staticmethod
    def add_item(cart_key, variant_id, quantity):
        try:
            variant = ProductVariant.objects.get(id=variant_id, is_active=True)
        except ProductVariant.DoesNotExist:
            raise ValueError('Variant not found or inactive')
        
        if quantity > variant.stock:
            raise ValueError('Insufficient stock')
        
        existing = redis_client.hget(cart_key, str(variant_id))
        if existing:
            quantity = int(existing) + quantity
            if quantity > variant.stock:
                quantity = variant.stock
                
        
        redis_client.hset(cart_key, str(variant_id), quantity)
        ttl = 60 * 60 * 24 * 30 if 'user' in cart_key else 60 * 60 * 24 * 7 
        redis_client.expire(cart_key, ttl)
        return redis_client.hgetall(cart_key)
        
    @staticmethod  
    def get_cart(cart_key):
        cart = redis_client.hgetall(cart_key)
        if not cart:
            return {'items': [], 'subtotal': 0}
        variant_ids = list(cart.keys())
        variants = ProductVariant.objects.filter(id__in=variant_ids)
        items = []
        sub_total = 0
        for variant in variants:
            quantity = int(cart[str(variant.id)])
            line_total = variant.price * quantity
            items.append({
                'variant_id': variant.id,
                'sku': variant.sku,
                'price': str(variant.price),
                'quantity': quantity,
                'line_total': str(line_total),
                'is_active': variant.is_active,
             })
            if variant.is_active:
                sub_total += line_total
            
        return {'items': items, 'subtotal': str(sub_total)}
    
    @staticmethod
    def update_quantity(cart_key, variant_id, quantity):
        try:
            variant = ProductVariant.objects.get(id=variant_id, is_active=True)
        except ProductVariant.DoesNotExist:
            raise ValueError('Product does not exist')
        
        if quantity == 0:
            redis_client.hdel(cart_key, str(variant_id))
            return redis_client.hgetall(cart_key)
        elif quantity > variant.stock:
            raise ValueError('Insufficient stock')

        redis_client.hset(cart_key, str(variant_id), quantity)
        ttl = 60 * 60 * 24 * 30 if 'user' in cart_key else 60 * 60 * 24 * 7 
        redis_client.expire(cart_key, ttl)
        return redis_client.hgetall(cart_key)
        
    @staticmethod
    def remove_items(cart_key, variant_id):
        redis_client.hdel(cart_key, str(variant_id))
        ttl = 60 * 60 * 24 * 30 if 'user' in cart_key else 60 * 60 * 24 * 7
        redis_client.expire(cart_key, ttl)
        return redis_client.hgetall(cart_key)
    
    @staticmethod
    def validate_cart(cart_key):
        cart = redis_client.hgetall(cart_key)
        if not cart:
            return {'valid': [], 'invalid': []}
        variant_ids = list(cart.keys())
        variants = ProductVariant.objects.filter(id__in=variant_ids).select_related('product')
        valid = []
        invalid = []
        for variant in variants:
            quantity = int(cart[str(variant.id)])
            if not variant.is_active or not variant.product.is_active:
                invalid.append({'variant_id': variant.id, 'reason': 'deactivated'})
            elif quantity> variant.stock:
                invalid.append({'variant_id': variant.id, 'reason': 'insufficient stock'})
            else:
                valid.append({'variant_id': variant.id, 'quantity': quantity}) 
        
        return {'valid': valid, 'invalid': invalid}               
                
        

    @staticmethod
    def merge_carts(user_id, session_token):
        guest_key = f'cart:guest:{session_token}'
        user_key = f'cart:user:{user_id}'
        
        guest_cart = redis_client.hgetall(guest_key)
        user_cart = redis_client.hgetall(user_key)
        
        if not guest_cart:
            return
        
        for variant_id, quantity in guest_cart.items():
            if variant_id in user_cart:
               new_quantity = int(user_cart[variant_id]) + int(quantity)
            else:
               new_quantity = int(quantity)
            redis_client.hset(user_key, variant_id, int(new_quantity) )     
        redis_client.delete(guest_key)
    
    @staticmethod
    def clear_cart(cart_key):
        redis_client.delete(cart_key)
        return True
    
    @staticmethod
    def calculate_total(cart_key):
        cart = redis_client.hgetall(cart_key)
        total = 0
        for item in cart:
            variant = ProductVariant.objects.get(id=item)
            quantity = int(cart[item])# for each variant_id, get the price from ProductVariant
            cost = variant.price * quantity# multiply price by quantity
            total += cost# sum everything up
        return total
                    
        