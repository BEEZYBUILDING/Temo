from django.shortcuts import render
from redis_client import redis_client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import get_cart_key
import uuid
# Create your views here.

class CartView(APIView):
    
    def get(self, request):
        cart_key = get_cart_key(request)
        cart = redis_client.hgetall(cart_key)
        return Response(cart, status=status.HTTP_200_OK)
    
    def post(self, request):
        session_token = request.headers.get('X-Session-Token')
        
        if not session_token:
            session_token = str(uuid.uuid4()) #generate a new session token
            
        cart_key = get_cart_key(request, session_token=session_token)
        variant_id = request.data.get('variant_id')
        quantity = request.data.get('quantity')
        redis_client.hset(cart_key, str(variant_id), quantity)
        redis_client.expire(cart_key, 60 * 60 * 24 * 7) #TTL, 7 days
        
        return Response({
            'cart': redis_client.hgetall(cart_key),
            'session_token': session_token
        }, status=status.HTTP_201_CREATED)