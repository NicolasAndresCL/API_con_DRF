from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import OrderItem, Order

@receiver(post_delete, sender=OrderItem)
@receiver(post_save, sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    """
    Actualiza el total_amount del pedido cuando un OrderItem es guardado o eliminado.
    """
    # Usamos try-except para manejar el caso en que la orden ya no exista (ej. CASCADE delete de la orden)
    try:
        instance.order.calculate_total_amount()
    except Order.DoesNotExist:
        pass # La orden ya fue eliminada, no hay nada que actualizar.