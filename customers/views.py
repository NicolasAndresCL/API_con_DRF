from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Customer
from .serializers import CustomerSerializer

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
        action_perm_map = {
            'list': AllowAny,
            'retrieve': AllowAny,
            'create': IsAuthenticated,
            'update': IsAdminUser,
            'partial_update': IsAdminUser,
            'destroy': IsAdminUser
        }
        permission_class = action_perm_map.get(self.action, IsAuthenticated)
        return [permission_class()]

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        has_pending_orders = instance.orders.filter(status='pending').exists()
        if has_pending_orders:
            raise ValidationError({"detail": "No se puede eliminar un cliente con pedidos pendientes."})
        instance.delete()
