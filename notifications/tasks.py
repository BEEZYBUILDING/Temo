from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from orders.models import Order

@shared_task(max_retries=3, default_retry_delay=60)
def send_order_confirmation_email(order_id):
    # fetch order from DB
    try:
        order = Order.objects.prefetch_related('items').get(id=order_id)
        # render template
        html_content = render_to_string('notifications/order_confirmation.html', {
            'order': order,
            'items': order.items.all(),
            'address': order.address,
        })
        # send email
        send_mail(
            subject=f'Order #{order.id} Confirmation',
            message='',
            from_email=None,  # uses DEFAULT_FROM_EMAIL
            recipient_list=[order.user.email],
            html_message=html_content,
        )
    except Exception as exc:
        raise send_order_confirmation_email.retry(exc=exc, countdown=60)