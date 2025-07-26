from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Customer
from .serializers import CustomerSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Listar clientes",
        description="Devuelve una lista completa de los clientes registrados.",
        tags=["Customers"]
    ),
    retrieve=extend_schema(
        summary="Obtener cliente",
        description="Devuelve los datos de un cliente específico por ID.",
        tags=["Customers"]
    ),
    create=extend_schema(
        summary="Crear cliente",
        description="Registra un nuevo cliente. Requiere autenticación.",
        tags=["Customers"]
    ),
    update=extend_schema(
        summary="Actualizar cliente",
        description="Reemplaza todos los datos de un cliente existente. Requiere permisos de administrador.",
        tags=["Customers"]
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente cliente",
        description="Modifica parcialmente los datos de un cliente. Requiere permisos de administrador.",
        tags=["Customers"]
    ),
    destroy=extend_schema(
        summary="Eliminar cliente",
        description="Elimina un cliente solo si no tiene pedidos pendientes. Requiere permisos de administrador.",
        tags=["Customers"]
    ),
)
class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        if instance.orders.filter(status='pending').exists():
            raise ValidationError({"detail": "No se puede eliminar un cliente con pedidos pendientes."})
        super().perform_destroy(instance)
