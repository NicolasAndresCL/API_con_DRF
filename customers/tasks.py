from celery import shared_task
from .models import Customer

@shared_task
def export_active_customers():
    return list(Customer.objects.filter(is_active=True).values('id', 'name'))

@shared_task
def saludo_desde_celery():
    print("Celery está funcionando correctamente 🚀")
    return "Hola desde la tarea asincrónica"