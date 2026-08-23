import stripe
from django.conf import settings
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(order):
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
    return intent.client_secret