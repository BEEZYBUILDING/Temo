from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order

@receiver(pre_save, sender=Order)
def store_previous_status(sender, instance, **kwargs):
    if instance.pk: #only if the order exists and is not new
        old_order = Order.objects.get(pk=instance.pk) #instance.pk checks if the order exists
        instance._previous_status = old_order.status
    else:
        instance._previous_status = None

#@receiver(post_save, sender=Order)
#def create_status_history(sender, instance, created, **kwargs):
#    if not created: #only for updates, not new orders
#        if instance._previous_status != instance.status:
#            OrderStatusHistory.objects.create(
#                order=instance,
#                previous_status=instance._previous_status,
#                new_status=instance.status,
#            )
