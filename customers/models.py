from django.db import models
from django.utils import timezone # Importar para usar timezone.now

# Modelo Customer con campos más profesionales
class Customer(models.Model):
    # Información de identificación del cliente
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    email = models.EmailField(max_length=254, unique=True, verbose_name="Correo Electrónico")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Número de Teléfono")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento")

    # Información de dirección (se mantiene aquí por simplicidad, aunque en apps más grandes,
    # Address podría ser un modelo separado con una ForeignKey a Customer)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección Línea 1")
    address_line_2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección Línea 2")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ciudad")
    state_province = models.CharField(max_length=100, blank=True, null=True, verbose_name="Estado/Provincia")
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Código Postal")
    country = models.CharField(max_length=100, default="Chile", verbose_name="País")

    # Campos de control y metadatos
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Registro")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    notes = models.TextField(blank=True, null=True, verbose_name="Notas Adicionales")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['last_name', 'first_name'] # Ordenar por apellido y luego por nombre

    def __str__(self):
        # Usamos full_name o una combinación de nombre y apellido
        # para una representación más profesional
        return f"{self.first_name} {self.last_name} ({self.email})"

    # Opcional: Propiedad para obtener el nombre completo (útil en Order.__str__)
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # Opcional: Propiedad para obtener la dirección completa en un formato legible
    @property
    def full_address(self):
        address = [self.address_line_1]
        if self.address_line_2:
            address.append(self.address_line_2)
        address.append(f"{self.city}, {self.state_province} {self.postal_code}")
        address.append(self.country)
        return ", ".join(filter(None, address)) # filter(None, ...) elimina elementos vacíos

# El modelo Order se mantiene, pero su __str__ se adapta al nuevo Customer
class Order(models.Model):
    # Relación de muchos a uno con Customer
    # Un cliente puede tener muchos pedidos, pero un pedido pertenece a un solo cliente.
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')

    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending') # 'pending', 'completed', 'cancelled'
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        # Adaptado para usar el nuevo atributo 'full_name' del cliente
        return f"Order {self.id} for {self.customer.full_name} - Status: {self.status}"


