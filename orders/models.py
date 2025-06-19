# models.py en la app orders

from django.db import models
from django.conf import settings
from customers.models import Customer
from products.models import Product  

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pendiente'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ], default='pending')

    def __str__(self):
        return f"Pedido {self.id} de {self.customer.full_name}"
    
    def calculate_total_amount(self):
        """Calcula el total del pedido sumando los OrderItems."""
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total or 0
        self.save()
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items') # Relaciona con Order
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # Relaciona con Product
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2) # Precio del producto en el momento de la compra

    class Meta:
        # Asegura que un mismo producto no se añada dos veces al mismo pedido como un OrderItem separado
        # Aunque esto puede ser manejado en la lógica del frontend/backend, es una buena práctica.
        unique_together = ('order', 'product')

    def save(self, *args, **kwargs):
        # Cuando se guarda un OrderItem, asegurar que el precio se tome del Product actual
        if not self.price_at_order: # Solo si no se ha establecido manualmente
            self.price_at_order = self.product.price
        super().save(*args, **kwargs)

        # Recalcular el total del pedido padre cada vez que se guarda/actualiza un item
        # self.order.calculate_total_amount() Ahora se maneja en signals.py

    @property
    def subtotal(self):
        return self.quantity * self.price_at_order

    def __str__(self):
        return f"{self.quantity} x {self.product.name} en Pedido {self.order.id}"
