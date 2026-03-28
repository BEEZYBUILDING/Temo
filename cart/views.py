from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import CartService
from .utils import get_cart_key
import uuid
# Create your views here.

class CartView(APIView):
    
    def get(self, request):
        cart_key = get_cart_key(request)
        cart = CartService.get_cart(cart_key)
        return Response(cart, status=status.HTTP_200_OK)
    
    def post(self, request):
        session_token = request.headers.get('X-Session-Token')
        
        if not session_token:
            session_token = str(uuid.uuid4()) #generate a new session token
            
        cart_key = get_cart_key(request, session_token=session_token)
        variant_id = request.data.get('variant_id')
        quantity = request.data.get('quantity')
        try:
            cart = CartService.add_item(cart_key=cart_key, variant_id=variant_id, quantity=quantity)
            return Response({
                'cart': cart,
                'session_token': session_token}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self, request):
        cart_key = get_cart_key(request)
        CartService.clear_cart(cart_key)
        return Response('Cart cleared', status=status.HTTP_200_OK)
        
class CartItemView(APIView):
    def put(self, request, variant_id):
        cart_key = get_cart_key(request)
        quantity = request.data.get('quantity')
        
        try:
            cart = CartService.update_quantity(cart_key, variant_id, quantity)
            return Response(cart, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, variant_id):
        cart_key = get_cart_key(request)
        
        cart = CartService.remove_items(cart_key, variant_id)
        return Response(cart, status=status.HTTP_200_OK)
    
class CartValidateView(APIView):
    
    def post(self, request):
        cart_key = get_cart_key(request)
        
        cart = CartService.validate_cart(cart_key)
        return Response(cart, status=status.HTTP_200_OK)