from django.db.models import Avg
from django.shortcuts import render
from products.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer, CreateReviewSerializer
from .services import check_verified_purchase, update_product_rating

# Create your views here.
class ReviewListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, product_id):
        review = Review.objects.filter(product_id=product_id).order_by('-created_at')
        serializer = ReviewSerializer(review, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return Response("Authentication Required", status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CreateReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response("Product not found", status=status.HTTP_404_NOT_FOUND)

        if not check_verified_purchase(request.user, product):
            return Response('You can  only review products that yo uhave purchased and received', status=status.HTTP_400_BAD_REQUEST)

        if Review.objects.filter(user=request.user, product=product).exists():
            return Response('You have already reviewed this product', status=status.HTTP_400_BAD_REQUEST)
        
        order_id = serializer.validated_data['order_id']
        review = Review.objects.create(
            user=request.user,
            product=product,
            order_id=order_id,
            rating=serializer.validated_data['rating'],
            title=serializer.validated_data['title'],
            body=serializer.validated_data.get('body', '')
        )
        update_product_rating(product_id)
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)       

class ReviewUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
                review = Review.objects.get(user=request.user, id=pk)
        except Review.DoesNotExist:
            return Response('Review not found', status=status.HTTP_404_NOT_FOUND)
        serializer = CreateReviewSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        review.rating = serializer.validated_data['rating']
        review.title = serializer.validated_data['title']
        review.body = serializer.validated_data.get('body', review.body)
        review.save()
        update_product_rating(review.product.id)

        return Response(ReviewSerializer(review).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            review = Review.objects.get(user=request.user, id=pk)
        except Review.DoesNotExist:
            return Response('Review not found', status=status.HTTP_404_NOT_FOUND)
            
        product = review.product
        review.delete()
        update_product_rating(product.id)
            
        avg_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
        return Response({'avg_rating': avg_rating}, status=status.HTTP_200_OK)