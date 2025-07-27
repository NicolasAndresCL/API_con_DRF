import logging
from celery import shared_task
from customers.models import Customer

logger = logging.getLogger(__name__)

def obtener_clientes_activos():
    """
    Retorna una lista de clientes activos con campos clave.
    """
    return list(
        Customer.objects.filter(is_active=True).values("id", "name")
    )

def generar_saludo():
    """
    Mensaje para verificar funcionamiento de tareas asincrónicas.
    """
    mensaje = "Celery está funcionando correctamente 🚀"
    logger.info(mensaje)
    return "Hola desde la tarea asincrónica"

@shared_task(name="clientes.exportar_activos")
def task_exportar_clientes_activos():
    """
    Tarea asincrónica que retorna clientes activos.
    Puede ser visualizada en Flower y disparada desde Swagger.
    """
    return obtener_clientes_activos()

@shared_task(name="clientes.saludo_test")
def task_saludo_desde_celery():
    """
    Tarea simple para testeo manual desde Swagger o admin Celery.
    """
    return generar_saludo()
