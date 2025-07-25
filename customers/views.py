from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from .models import Customer
from .serializers import CustomerSerializer

@extend_schema(
    tags=["Customers"],
    summary="Gestión de clientes",
    description="CRUD completo de clientes con permisos diferenciados según la acción.",
    responses={200: CustomerSerializer}
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
