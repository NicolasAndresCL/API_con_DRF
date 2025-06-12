# products/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny # Importa las clases de permiso
from rest_framework.response import Response
from rest_framework.decorators import action # Para acciones personalizadas
from django.db import transaction # Para asegurar la atomicidad de las operaciones

from .models import Product
from .serializers import ProductSerializer
from products import serializers

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            # Cualquiera puede listar y ver detalles de productos
            permission_classes = [AllowAny]
        else:
            # Para crear, actualizar, eliminar, se requiere autenticación
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes] 

    def perform_create(self, serializer):
        # Lógica de negocio antes de crear un producto
        # Por ejemplo, asegurar que el stock inicial no es negativo
        stock = serializer.validated_data.get('stock', 0)
        if stock < 0:
            # Puedes levantar una excepción que DRF convertirá en un error 400
            raise serializers.ValidationError({"stock": "El stock inicial no puede ser negativo."})

        # Si el stock es 0, automáticamente marcarlo como inactivo al crear
        if stock == 0:
            serializer.validated_data['is_active'] = False

        # Guarda el objeto usando el ORM de Django
        serializer.save()

    def perform_update(self, serializer):
        # Lógica de negocio antes de actualizar un producto
        # Puedes acceder al objeto original usando serializer.instance
        old_stock = serializer.instance.stock
        new_stock = serializer.validated_data.get('stock', old_stock)

        # Asegurar que el stock nunca se vuelve negativo
        if new_stock < 0:
            raise serializers.ValidationError({"stock": "El stock no puede ser negativo."})

        # Lógica: Si el stock pasa a 0, marcar el producto como inactivo
        if old_stock > 0 and new_stock == 0:
            serializer.validated_data['is_active'] = False
        # Lógica: Si el stock era 0 y ahora es > 0, marcarlo como activo (opcional)
        elif old_stock == 0 and new_stock > 0:
            serializer.validated_data['is_active'] = True

        # Guarda el objeto actualizado
        serializer.save()

    # Ejemplo de acción personalizada: Marcar un producto como agotado
    # Esto creará una ruta PUT en /api/products/{id}/mark_sold_out/
    @action(detail=True, methods=['put'])
    def mark_sold_out(self, request, pk=None):
        try:
            # transaction.atomic() asegura que todas las operaciones dentro del bloque
            # se completen con éxito o ninguna lo haga (rollback).
            with transaction.atomic():
                product = self.get_object() # Obtiene el producto por su ID
                if product.stock == 0 and not product.is_active:
                    return Response({"detail": "El producto ya está agotado."}, status=status.HTTP_400_BAD_REQUEST)

                product.stock = 0
                product.is_active = False
                product.save()

                # Retorna el producto actualizado
                serializer = self.get_serializer(product)
                return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Ejemplo de acción personalizada: Incrementar el stock de un producto
    # Esto creará una ruta POST en /api/products/{id}/increase_stock/
    @action(detail=True, methods=['post'])
    def increase_stock(self, request, pk=None):
        amount = request.data.get('amount', 1)
        try:
            amount = int(amount)
            if amount <= 0:
                return Response({"amount": "La cantidad debe ser un número positivo."}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({"amount": "La cantidad debe ser un número entero."}, status=status.HTTP_400_BAD_REQUEST)

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