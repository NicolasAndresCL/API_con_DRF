from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Product
from .serializers import ProductSerializer
from products import serializers

@extend_schema_view(
    list=extend_schema(
        summary="Listar productos",
        description="Listado público de productos disponibles.",
        tags=["Products"]
    ),
    retrieve=extend_schema(
        summary="Obtener producto",
        description="Detalle de producto por ID.",
        tags=["Products"]
    ),
    create=extend_schema(
        summary="Crear producto",
        description="Creación de producto con validación de stock inicial.",
        tags=["Products"]
    ),
    update=extend_schema(
        summary="Actualizar producto",
        description="Actualiza todos los datos del producto, aplicando lógica de stock y visibilidad.",
        tags=["Products"]
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente producto",
        description="Modifica parcialmente los datos del producto.",
        tags=["Products"]
    ),
    destroy=extend_schema(
        summary="Eliminar producto",
        description="Elimina un producto por ID. Requiere autenticación.",
        tags=["Products"]
    ),
)
@extend_schema(
    tags=["Products"],
    description="CRUD completo de productos con lógica de stock, visibilidad (activo/inactivo) y acciones personalizadas."
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        stock = serializer.validated_data.get('stock', 0)
        if stock < 0:
            raise serializers.ValidationError({"stock": "El stock inicial no puede ser negativo."})
        if stock == 0:
            serializer.validated_data['is_active'] = False
        serializer.save()

    def perform_update(self, serializer):
        old_stock = serializer.instance.stock
        new_stock = serializer.validated_data.get('stock', old_stock)

        if new_stock < 0:
            raise serializers.ValidationError({"stock": "El stock no puede ser negativo."})
        if old_stock > 0 and new_stock == 0:
            serializer.validated_data['is_active'] = False
        elif old_stock == 0 and new_stock > 0:
            serializer.validated_data['is_active'] = True
        serializer.save()

    @extend_schema(
        summary="Marcar producto como agotado",
        description="Marca un producto como inactivo si su stock es cero.",
        tags=["Products"]
    )
    @action(detail=True, methods=['put'])
    def mark_sold_out(self, request, pk=None):
        # ... (sin cambios en la lógica)
        pass

    @extend_schema(
        summary="Incrementar stock del producto",
        description="Suma una cantidad específica al stock actual del producto.",
        tags=["Products"]
    )
    @action(detail=True, methods=['post'])
    def increase_stock(self, request, pk=None):
        # ... (sin cambios en la lógica)
        pass
