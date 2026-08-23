import stripe
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from orders.models import Order
from orders.services import update_order_status
from .models import Payment
from .serializers import CreatePaymentIntentSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CreatePaymentIntentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        order_id = serializer.validated_data['order_id']
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response('Order not found', status=status.HTTP_404_NOT_FOUND)

        if order.status != 'PENDING':
            return Response('Order is not pending', status=status.HTTP_400_BAD_REQUEST)

        # Step 3 - create PaymentIntent with Stripe
        intent = stripe.PaymentIntent.create(
            amount=int(order.total * 100),  # convert to cents
            currency='usd',
            metadata={'order_id': order.id}
        )

        # Step 4 - create Payment record
        Payment.objects.create(
            order=order,
            stripe_payment_intent_id=intent.id,
            amount=order.total,
            currency='usd',
            status='PENDING'
        )

        # Step 5 - return client_secret
        return Response({
            'client_secret': intent.client_secret
        }, status=status.HTTP_201_CREATED)

class StripeWebhookView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except stripe.error.SignatureVerificationError:
            return Response('Invalid signature', status=status.HTTP_400_BAD_REQUEST)
        
        # get event type and payment intent
        event_type = event['type']
        payment_intent = event['data']['object']
        payment_intent_id = payment_intent['id']
        
        # look up payment record
        try:
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent_id)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_200_OK)
                    # idempotency check
        if payment.status != 'PENDING':
            return Response(status=status.HTTP_200_OK)
        
        # handle payment succeeded
        if event_type == 'payment_intent.succeeded':
            payment.status = 'SUCCEEDED'
            payment.save()
            update_order_status(payment.order, 'CONFIRMED')
        
        # handle payment failed
        elif event_type == 'payment_intent.payment_failed':
            payment.status = 'FAILED'
            payment.save()
            update_order_status(payment.order, 'PAYMENT_FAILED')
        
        return Response(status=status.HTTP_200_OK)
            