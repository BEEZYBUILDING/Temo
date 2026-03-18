from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import render
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import IsAdmin
from .filters import ProductFilter
from .models import Product, ProductVariant, ProductImage
from .serializers import ProductSerializer, ProductVariantSerializer, ProductImageSerializer

# Create your views here.
class ProductView(APIView):
    #permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering = ['-created_at'] #default
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [] #this means no permission required
        return [IsAdmin()] #admin for everything else apart from the GET function
    
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
        
    def get(self, request):
        queryset = Product.objects.filter(is_active=True)
        filtered_queryset = ProductFilter(request.GET, queryset=queryset).qs
        
        search_query = request.GET.get('search') #gets the word the user wants to search for
        if search_query:
            vector = SearchVector('name', weight='A') + SearchVector('description', weight='B') #sets parameter(A, B) to the weight
            query = SearchQuery(search_query)#it searches for the word
            filtered_queryset = filtered_queryset.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.1).order_by('-rank') # find the word adds wach word found and arrnages it by rank
        
        serializer = ProductSerializer(filtered_queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

        
    
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