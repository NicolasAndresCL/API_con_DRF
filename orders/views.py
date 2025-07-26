from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Order
from .serializers import OrderSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Listar órdenes",
        description="Devuelve todas las órdenes registradas, con datos de cliente y productos.",
        tags=["Orders"]
    ),
    retrieve=extend_schema(
        summary="Obtener orden",
        description="Devuelve una orden específica por ID, incluyendo cliente y productos relacionados.",
        tags=["Orders"]
    ),
    create=extend_schema(
        summary="Crear orden",
        description="Registra una nueva orden asociada a un cliente. Puede incluir múltiples productos.",
        tags=["Orders"]
    ),
    update=extend_schema(
        summary="Actualizar orden",
        description="Reemplaza completamente los datos de una orden existente.",
        tags=["Orders"]
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente orden",
        description="Modifica parcialmente los datos de una orden existente.",
        tags=["Orders"]
    ),
    destroy=extend_schema(
        summary="Eliminar orden",
        description="Elimina una orden por ID. Puede estar restringido según estado o relaciones.",
        tags=["Orders"]
    ),
)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
