from cart.services import CartService
from cart.utils import get_cart_key
from decimal import Decimal
from django.shortcuts import render
from django.db import transaction
from payments.services import create_payment_intent
from products.models import ProductVariant
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Address
from users.permissions import IsAdmin
from .filters import OrderFilter
from .models import Order, OrderItem, Coupon, OrderStatusHistory
from .pagination import OrderPagination
from .serializers import CheckoutSerializer, OrderListSerializer, OrderDetailSerializer
from .services import update_order_status

# Create your views here.
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

        cart_key = get_cart_key(request)
        cart = CartService.get_cart(cart_key)

        if not cart['items']:
            return Response('Cart is empty', status=status.HTTP_400_BAD_REQUEST)

        address_id = serializer.validated_data['address_id']
        try: 
            address = Address.objects.get(id=address_id,user=request.user)
            address_snapshot = {
                'full_name': address.full_name,
                'phone': address.phone,
                'street': address.street,
                'city': address.city,
                'state': address.state,
                'country': address.country,
                'postal_code': address.postal_code,
            }
        except Address.DoesNotExist:
            return Response('Invalid Address', status=status.HTTP_404_NOT_FOUND)

      

        subtotal = Decimal(cart['subtotal'])
        shipping = Decimal('0') if subtotal >= 100 else Decimal('10')

        tax_amount = Decimal('0.075') * subtotal
        total = subtotal + shipping + tax_amount

        coupon = None
        discount_amount = Decimal('0')
        coupon_code = serializer.validated_data.get('coupon_code')

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code.upper())
                coupon.is_valid(subtotal)

                if coupon.discount_type == 'FLAT':
                    discount_amount = coupon.discount_value
                elif coupon.discount_type == 'PERCENTAGE':
                    discount_amount = subtotal * (coupon.discount_value/100)
                total = total - discount_amount

            except Coupon.DoesNotExist:
                return Response('Invalid coupon', status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    address=address_snapshot,
                    subtotal=subtotal,
                    shipping_cost=shipping,
                    tax_amount=tax_amount,
                    discount_amount=discount_amount,
                    total=total,
                )
                
                for item in cart['items']:
                    variant = ProductVariant.objects.select_for_update().get(id=item['variant_id'])
                    if variant.stock < item['quantity']:
                        raise ValueError(f'{variant.sku} is out of stock')
                    variant.stock -= item['quantity']
                    variant.save()
                    OrderItem.objects.create(
                        order=order,                              # the order we just created
                        variant=variant,                          # from database
                        product_name=variant.product.name,        # snapshot from database
                        variant_attributes=variant.attributes,    # snapshot from database
                        quantity=item['quantity'],                # from cart
                        unit_price=Decimal(item['price']),        # snapshot from cart
                        line_total=Decimal(item['line_total']),   # from cart
                    )
                if coupon:
                    coupon.current_uses +=1
                    coupon.save()

            CartService.clear_cart(cart_key)
            client_secret = create_payment_intent(order)
            return Response(
                {
                    'order_id': order.id,
                    'status': order.status,
                    'total': str(order.total),
                    'client_secret': client_secret
                }, status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class AdminOrderListView(APIView):
    
    permission_classes = [IsAdmin]
    def get(self, request):
        queryset = Order.objects.all()
        filtered_queryset = OrderFilter(request.GET, queryset=queryset).qs

        paginator = OrderPagination()
        page = paginator.paginate_queryset(filtered_queryset, request)
        serializer = OrderListSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

class AdminOrderDetailView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request, pk):
   
        try:
            order = Order.objects.select_related('user').prefetch_related(
                'items__variant__product',
                'history'
            ).get(id=pk)
        except Order.DoesNotExist:
            return Response("Order does not exist", status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminOrderStatusView(APIView):
    permission_classes = [IsAdmin]

    def put(self, request, pk):
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response("Order does not exist", status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('new_status')
        note = request.data.get('note')

        try:
            update_order_status(order, new_status, changed_by=request.user, note=note)
        except ValueError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)

        except Order.DoesNotExist:
            return Response("Order does not exist", status=status.HTTP_404_NOT_FOUND)

        if order.status not in ['PENDING', 'CONFIRMED']:
            return Response(
                "Order cannot be cancelled", status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            for item in order.items.all():
                variant = ProductVariant.objects.select_for_update().get(id=item.variant.id)
                variant.stock += item.quantity
                variant.save()
            update_order_status(order, 'CANCELLED', changed_by=request.user, note='Cancelled by user')
        return Response(OrderDetailSerializer(order).data, status=status.HTTP_200_OK)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.select_related('user').prefetch_related(
                'items__variant__product',
                'history'
            ).get(id=pk, user=request.user)
        except Order.DoesNotExist:
            return Response("Order does not exist", status=status.HTTP_404_NOT_FOUND)

        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Order.objects.filter(user=request.user).order_by('-created_at')
        paginator = OrderPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = OrderListSerializer(page, many=True)
        
        return paginator.get_paginated_response(serializer.data)

class AdminCouponListCreateView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        queryset = Coupon.objects.all()
        serializer = CouponSerializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminCouponUpdateDeleteView(APIView):
    permission_classes = [IsAdmin]

    def put(self, request, pk):
        try:
            coupon = Coupon.objects.get(id=pk)
        except Coupon.DoesNotExist:
            return Response('Coupon not found', status=status.HTTP_404_NOT_FOUND)
        
        serializer = CouponSerializer(coupon, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            coupon = Coupon.objects.get(id=pk)
        except Coupon.DoesNotExist:
            return Response('Coupon not found', status=status.HTTP_404_NOT_FOUND)
        
        coupon.is_active = False
        coupon.save()
        return Response('Coupon deactivated', status=status.HTTP_200_OK)