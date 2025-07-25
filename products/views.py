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
    list=extend_schema(description="Listado público de productos disponibles."),
    retrieve=extend_schema(description="Detalle de producto por ID."),
    create=extend_schema(description="Creación de producto con validación de stock."),
    update=extend_schema(description="Actualización de producto con lógica de stock."),
    partial_update=extend_schema(description="Actualización parcial del producto."),
    destroy=extend_schema(description="Eliminación de producto (requiere autenticación)."),
)
@extend_schema(
    tags=["Products"],
    description="CRUD de productos con lógica de stock y disponibilidad activa/inactiva."
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
        description="Marca un producto como agotado si su stock es cero."
    )
    @action(detail=True, methods=['put'])
    def mark_sold_out(self, request, pk=None):
        try:
            with transaction.atomic():
                product = self.get_object()
                if product.stock == 0 and not product.is_active:
                    return Response({"detail": "El producto ya está agotado."}, status=status.HTTP_400_BAD_REQUEST)

                product.stock = 0
                product.is_active = False
                product.save()
                serializer = self.get_serializer(product)
                return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        description="Incrementa el stock del producto en una cantidad específica (por defecto, 1)."
    )
    @action(detail=True, methods=['post'])
    def increase_stock(self, request, pk=None):
        amount = request.data.get('amount', 1)
        try:
            amount = int(amount)
            if amount <= 0:
                return Response({"amount": "La cantidad debe ser positiva."}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({"amount": "Debe ser un número entero."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                product = self.get_object()
                product.stock += amount
                product.save()
                serializer = self.get_serializer(product)
                return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
