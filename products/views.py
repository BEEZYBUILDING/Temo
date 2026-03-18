from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import IsAdmin
from .models import Product, ProductVariant, ProductImage
from .serializers import ProductSerializer, ProductVariantSerializer, ProductImageSerializer

# Create your views here.
class ProductView(APIView):
    permission_classes = [IsAdmin]
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductSerializer(product, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            product.is_active = False
            product.save()
            return Response("Product deactivated", status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response("product not found", status=status.HTTP_404_NOT_FOUND)
        
        
class VariantView(APIView):
    permission_classes = [IsAdmin]
    
    def post(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response("Invalid Request", status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductVariantSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, variant_id):
        try:
            variant = ProductVariant.objects.get(id=variant_id, product=pk)
        except ProductVariant.DoesNotExist:
            return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductVariantSerializer(variant, data=request.data) # for updates pass the existing objects as the first argument
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ProductImageView(APIView):
    permission_classes = [IsAdmin]
    
    def post(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductImageSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)