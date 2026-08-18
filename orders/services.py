from .models import Order, OrderStatusHistory

def update_order_status(order, new_status, changed_by=None, note=None):
    previous_status = order.status
    try:
        order.transition_to(new_status)
    except ValueError as e:
        raise

    OrderStatusHistory.objects.create(
        order=order,
        previous_status=previous_status,  
        new_status=new_status,
        changed_by=changed_by,
        note=note
    )
    return order