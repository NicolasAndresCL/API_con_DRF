# customers/models.py
from django.db import models

# Create your models here.
class Customer(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
# Nuevo modelo Order 
class Order(models.Model):
    # Relación de muchos a uno con Customer
    # Un cliente puede tener muchos pedidos, pero un pedido pertenece a un solo cliente.
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending') # 'pending', 'completed', 'cancelled'
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} for {self.customer.title} - Status: {self.status}"
