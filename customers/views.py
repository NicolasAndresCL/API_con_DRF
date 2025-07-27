# customers/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema_view, extend_schema
from customers.models import Customer
from customers.serializers import CustomerSerializer, SaludoResponseSerializer
from customers.services.tasks import (
    task_exportar_clientes_activos,
    task_saludo_desde_celery
)

# 📚 ViewSet con documentación Swagger
@extend_schema_view(
    list=extend_schema(summary="Listar clientes", description="Devuelve todos los clientes registrados.", tags=["Customers"]),
    retrieve=extend_schema(summary="Obtener cliente", description="Muestra un cliente por ID.", tags=["Customers"]),
    create=extend_schema(summary="Crear cliente", description="Registra un nuevo cliente. Requiere autenticación.", tags=["Customers"]),
    update=extend_schema(summary="Actualizar cliente", description="Reemplaza todos los datos. Requiere permisos de administrador.", tags=["Customers"]),
    partial_update=extend_schema(summary="Actualización parcial", description="Modifica algunos campos. Requiere permisos de administrador.", tags=["Customers"]),
    destroy=extend_schema(summary="Eliminar cliente", description="Solo si no tiene pedidos pendientes. Requiere permisos de administrador.", tags=["Customers"]),
)
class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        permission_map = {
            "list": AllowAny,
            "retrieve": AllowAny,
            "create": IsAuthenticated,
            "update": IsAdminUser,
            "partial_update": IsAdminUser,
            "destroy": IsAdminUser,
        }
        return [permission_map.get(self.action, IsAuthenticated)()]

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        if instance.orders.filter(status="pending").exists():
            raise ValidationError({"detail": "No se puede eliminar un cliente con pedidos pendientes."})
        instance.delete()


@extend_schema_view(
    get=extend_schema(
        summary="Lanza saludo de prueba vía Celery",
        responses=SaludoResponseSerializer,
        tags=["Tasks"],
        description="Dispara tarea asincrónica para verificar funcionamiento del worker Celery."
    )
)
@api_view(["GET"])
def trigger_saludo(request):
    task_saludo_desde_celery.delay()
    return Response({"message": "Tarea lanzada correctamente 🚀"})


@extend_schema_view(
    get=extend_schema(
        summary="Exporta clientes activos vía Celery",
        tags=["Tasks"],
        description="Dispara tarea asincrónica que filtra clientes activos y retorna sus datos esenciales."
    )
)
@api_view(["GET"])
def trigger_export(request):
    task_exportar_clientes_activos.delay()
    return Response({"status": "Exportación en curso..."})