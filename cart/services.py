from redis_client import redis_client
from products.models import ProductVariant

class CartService:
    
    @staticmethod
    def add_item(cart_key, variant_id, quantity):
        redis_client.hset(cart_key, str(variant_id), quantity)
        redis_client.expire(cart_key, 60 * 60 * 24 * 7 )
        return redis_client.hgetall(cart_key)
        
    @staticmethod  
    def get_cart(cart_key):
        return redis_client.hgetall(cart_key)
    
    @staticmethod
    def update_quantity(cart_key, variant_id, quantity):
        redis_client.hset(cart_key, str(variant_id), quantity)
        return redis_client.hgetall(cart_key)
        
    @staticmethod
    def remove_items(cart_key, variant_id):
        return redis_client.hdel(cart_key, str(variant_id))
    
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
                    
        