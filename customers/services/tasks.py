# customers/services/tasks.py

from celery import shared_task
from customers.models import Customer
import logging

logger = logging.getLogger(__name__)

# 📦 Lógica de negocio (reutilizable y testeable)
def obtener_clientes_activos():
    """
    Retorna una lista de clientes activos con campos clave.
    """
    clientes = Customer.objects.filter(is_active=True).values('id', 'name')
    return list(clientes)

def generar_saludo():
    """
    Ejecuta una acción de saludo para verificar funcionamiento de tareas asincrónicas.
    """
    mensaje = "Celery está funcionando correctamente 🚀"
    logger.info(mensaje)  # Se puede ver en Flower o logs de worker
    return "Hola desde la tarea asincrónica"

# 🔁 Tareas registradas en Celery
@shared_task(name="clientes.exportar_activos")
def task_exportar_clientes_activos():
    """
    Tarea asincrónica que retorna clientes activos.
    """
    return obtener_clientes_activos()

@shared_task(name="clientes.saludo_test")
def task_saludo_desde_celery():
    """
    Tarea asincrónica de verificación rápida.
    """
    return generar_saludo()
