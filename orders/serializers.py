import decimal # Importante para manejar precios con decimales
from rest_framework import serializers
from products.models import Product
from .models import Order, OrderItem

from products.serializers import ProductSerializer 

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) 
    # product_id es el campo que el cliente enviará para crear/actualizar un OrderItem.
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), 
        write_only=True # <-- ¡Crucial para que no aparezca en la respuesta!
    )
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price_at_order']
       
        read_only_fields = ['price_at_order'] # El cliente no debe enviar este campo, se calcula automáticamente.
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad de un ítem debe ser un número positivo.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    # many=True indica que esperamos una lista de objetos OrderItem.
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_date', 'total_amount', 'status', 'items']
        
        # ***** CAMBIOS CLAVE AQUÍ *****
        # 1. 'order_date': auto_now_add=True en el modelo, el cliente no lo envía.
        # 2. 'total_amount': Es un campo calculado, el cliente no lo envía.
        # 3. 'status': Generalmente, el estado inicial es 'pending' por defecto en el modelo.
        #    Si el cliente no debe poder elegir el estado inicial, hazlo read_only.
        #    Si quieres que pueda, quítalo de aquí y considera una validación para los estados permitidos.
        read_only_fields = ['order_date', 'total_amount', 'status'] 
        # ******************************

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(total_amount=decimal.Decimal('0.00'), **validated_data) # Crea la Order sin total_amount, que se calculará después. 
        for item_data in items_data:
            # 'product_id' en item_data ya es un objeto Product gracias a PrimaryKeyRelatedField.
            # No es necesario hacer un Product.objects.get() aquí.
            product_instance = item_data.pop('product_id') # Extrae el objeto Product
            OrderItem.objects.create(
                order=order, # Asocia el item a la Order que acabamos de crear
                product=product_instance, # Usa el objeto Product validado
                **item_data # Resto de los datos del item (quantity)
            )
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', []) # Usa .pop con default para no fallar si no hay items en el PUT/PATCH

        instance.customer = validated_data.get('customer', instance.customer)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if items_data:
            instance.items.all().delete() # Borra todos los items existentes
            for item_data in items_data:
                product_instance = item_data.pop('product_id')
                OrderItem.objects.create(
                    order=instance,
                    product=product_instance,
                    **item_data
                )
        
        # Después de cualquier cambio en los OrderItems, el total de la Order
        # se recalculará automáticamente gracias a las señales.
        instance.refresh_from_db() # Para que el objeto instance en memoria refleje el total actualizado

        return instance