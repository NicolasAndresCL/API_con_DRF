# customers/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError # <-- Importa ValidationError de DRF
from .models import Customer, Order # Asegúrate de importar Order
from .serializers import CustomerSerializer

class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Customer.objects.all()
        return Customer.objects.none()

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        # Ahora que el atributo 'orders' (o 'order_set' si no usas related_name) existe,
        # podemos filtrar en él.
        # Usa 'orders' si lo definiste en related_name en el ForeignKey del modelo Order.
        # Si no definiste related_name, sería 'order_set'.
        if instance.orders.filter(status='pending').exists(): # Usamos 'orders' asumiendo related_name='orders'
            raise ValidationError( # Usamos ValidationError de rest_framework.exceptions
                {"detail": "No se puede eliminar un cliente con pedidos pendientes."}
            )
        super().perform_destroy(instance) # Llama al método destroy original
