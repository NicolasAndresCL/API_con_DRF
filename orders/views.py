from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from .models import Order
from .serializers import OrderSerializer

@extend_schema(
    tags=["Orders"],
    description="CRUD completo para órdenes registradas. Cada orden está asociada a un cliente y puede contener múltiples productos.",
)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
