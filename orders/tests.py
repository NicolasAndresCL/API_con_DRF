import decimal # Importa el módulo decimal para manejar números con coma flotante de forma precisa

from django.test import TestCase
from django.utils import timezone # Útil para manejar fechas y horas
from django.db.utils import IntegrityError # Para probar restricciones de unicidad

# Importa tus modelos de las apps correspondientes
from customers.models import Customer
from products.models import Product
from .models import Order, OrderItem

class OrderModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Order.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Configura datos que serán usados una vez para todas las pruebas de esta clase.
        Es más eficiente para datos que no cambian entre tests.
        """
        cls.customer = Customer.objects.create(
            first_name='Juan',
            last_name='Pérez',
            email='juan.perez@example.com',
            phone_number='123456789'
        )
        cls.product1 = Product.objects.create(
            name='Laptop XYZ',
            description='Potente laptop para trabajo y juegos',
            price=decimal.Decimal('1200.00'),
            stock=100
        )
        cls.product2 = Product.objects.create(
            name='Mouse Ergonómico',
            description='Mouse cómodo para largas horas de uso',
            price=decimal.Decimal('25.50'),
            stock=200
        )

    def setUp(self):
        """
        Configuración que se ejecuta ANTES de cada método de prueba.
        Aquí creamos datos que deben ser frescos para cada test.
        """
        # Reinicia el contador de Order para asegurar IDs predecibles en los tests si fuera necesario
        # Esto es más relevante si Order tuviera un contador global como en tu ejemplo anterior de Libro
        # En Django, el ID es auto-incremental de la DB, así que no es tan crítico a menos que tengas un contador manual.
        # En este caso, simplemente creamos una orden base.
        self.order = Order.objects.create(
            customer=self.customer,
            total_amount=decimal.Decimal('0.00') # El total inicial siempre debería ser 0
        )

    def test_order_creation(self):
        """Asegura que un Order se puede crear correctamente."""
        self.assertIsInstance(self.order, Order)
        self.assertEqual(self.order.customer, self.customer)
        self.assertIsNotNone(self.order.order_date) # order_date se auto-agrega
        self.assertEqual(self.order.total_amount, decimal.Decimal('0.00')) # Inicialmente 0
        self.assertEqual(self.order.status, 'pending')

    def test_order_str_representation(self):
        """Asegura que el método __str__ de Order devuelve el string esperado."""
        expected_str = f"Pedido {self.order.id} de {self.customer.full_name}"
        self.assertEqual(str(self.order), expected_str)

    def test_calculate_total_amount_no_items(self):
        """
        Prueba calculate_total_amount cuando no hay OrderItems asociados.
        Debe establecer total_amount a 0.
        """
        # La orden ya se creó en setUp sin items.
        self.order.calculate_total_amount()
        self.assertEqual(self.order.total_amount, decimal.Decimal('0.00'))

    def test_calculate_total_amount_with_items(self):
        """
        Prueba calculate_total_amount con OrderItems asociados.
        """
        # Añadir items a la orden
        OrderItem.objects.create(
            order=self.order,
            product=self.product1,
            quantity=2,
            price_at_order=self.product1.price # Usar el precio del producto
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product2,
            quantity=3,
            price_at_order=self.product2.price
        )

        # La lógica de save de OrderItem ya llama a calculate_total_amount,
        # pero podemos llamarla explícitamente para asegurar.
        self.order.calculate_total_amount()
        
        # Calcular el total esperado manualmente
        expected_total = (self.product1.price * 2) + (self.product2.price * 3)
        self.assertEqual(self.order.total_amount, expected_total)
        
        # Recargar la orden desde la base de datos para asegurar que el save() funcionó
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_amount, expected_total)

    def test_order_status_choices(self):
        """Asegura que los estados de la orden son válidos."""
        valid_statuses = [choice[0] for choice in Order._meta.get_field('status').choices]
        self.assertIn('pending', valid_statuses)
        self.assertIn('shipped', valid_statuses)
        self.assertIn('delivered', valid_statuses)
        self.assertIn('cancelled', valid_statuses)

        # Prueba asignar un estado y guardarlo
        self.order.status = 'shipped'
        self.order.save()
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'shipped')

        # Prueba asignar un estado inválido (esto lo validaría Django a nivel de formulario/serializer,
        # pero a nivel de modelo Python no siempre lanza error al asignar, aunque la DB podría fallar)
        # Para modelos, es mejor confiar en la validación de Django o probar con save()
        # Con `full_clean()` podemos forzar la validación del modelo
        with self.assertRaises(Exception): # Usamos Exception porque puede ser ValidationError u otro
             self.order.status = 'invalid_status'
             self.order.full_clean() # Ejecuta validadores del modelo
             self.order.save() # Intentar guardar



class OrderItemModelTest(TestCase):
    """
    Pruebas unitarias para el modelo OrderItem.
    """

    @classmethod
    def setUpTestData(cls):
        """Configuración de datos para todas las pruebas de OrderItem."""
        cls.customer = Customer.objects.create(
            first_name='Ana', last_name='Gómez', email='ana.gomez@example.com'
        )
        cls.product_a = Product.objects.create(
            name='Teclado Mecánico', price=decimal.Decimal('80.00'), stock=50
        )
        cls.product_b = Product.objects.create(
            name='Monitor UltraWide', price=decimal.Decimal('350.00'), stock=20
        )
    
    def setUp(self):
        """Configuración antes de cada prueba de OrderItem."""
        self.order = Order.objects.create(customer=self.customer, total_amount=decimal.Decimal('0.00'))

    def test_order_item_creation(self):
        """Asegura que un OrderItem se puede crear correctamente."""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product_a,
            quantity=1,
            price_at_order=decimal.Decimal('80.00') # Omitirlo para que se tome del producto
        )
        self.assertIsInstance(order_item, OrderItem)
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product_a)
        self.assertEqual(order_item.quantity, 1)
        self.assertEqual(order_item.price_at_order, decimal.Decimal('80.00'))
        self.assertEqual(order_item.subtotal, decimal.Decimal('80.00')) # 1 * 80.00

    def test_order_item_str_representation(self):
        """Asegura que el método __str__ de OrderItem devuelve el string esperado."""
        order_item = OrderItem.objects.create(
            order=self.order, product=self.product_a, quantity=2, price_at_order=self.product_a.price
        )
        expected_str = f"2 x {self.product_a.name} en Pedido {self.order.id}"
        self.assertEqual(str(order_item), expected_str)

    def test_subtotal_calculation(self):
        """Prueba que el subtotal se calcula correctamente."""
        order_item = OrderItem.objects.create(
            order=self.order, product=self.product_a, quantity=5, price_at_order=decimal.Decimal('80.00')
        )
        self.assertEqual(order_item.subtotal, decimal.Decimal('400.00')) # 5 * 80.00

        # Prueba con otra cantidad y precio
        order_item.quantity = 3
        order_item.price_at_order = decimal.Decimal('75.00')
        self.assertEqual(order_item.subtotal, decimal.Decimal('225.00')) # 3 * 75.00

    def test_price_at_order_auto_set_on_save(self):
        """
        Asegura que price_at_order se establece automáticamente si no se provee.
        """
        # Crear OrderItem sin especificar price_at_order
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product_a,
            quantity=1
        )
        self.assertEqual(order_item.price_at_order, self.product_a.price)

        # Si se provee, debe respetar el valor provisto
        custom_price = decimal.Decimal('70.00')
        order_item_custom_price = OrderItem.objects.create(
            order=self.order,
            product=self.product_b,
            quantity=1,
            price_at_order=custom_price
        )
        self.assertEqual(order_item_custom_price.price_at_order, custom_price)


    def test_order_total_amount_update_on_order_item_save(self):
        """
        Asegura que el total del pedido se actualiza automáticamente
        cuando se guarda un OrderItem nuevo.
        """
        # La orden se inicia con total_amount=0 en setUp
        self.assertEqual(self.order.total_amount, decimal.Decimal('0.00'))

        # Guardar el primer item: 2 * 80.00 = 160.00
        OrderItem.objects.create(
            order=self.order,
            product=self.product_a,
            quantity=2,
            price_at_order=self.product_a.price
        )
        self.order.refresh_from_db() # Recargar la orden para obtener el total actualizado
        self.assertEqual(self.order.total_amount, decimal.Decimal('160.00'))

        # Guardar un segundo item: 3 * 350.00 = 1050.00
        # El total esperado será 160.00 + 1050.00 = 1210.00
        OrderItem.objects.create(
            order=self.order,
            product=self.product_b,
            quantity=3,
            price_at_order=self.product_b.price
        )
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_amount, decimal.Decimal('1210.00'))
    
    def test_order_total_amount_update_on_order_item_update(self):
        """
        Asegura que el total del pedido se actualiza cuando
        un OrderItem existente es modificado.
        """
        # Crear un item inicial
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product_a,
            quantity=1,
            price_at_order=self.product_a.price
        )
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_amount, self.product_a.price) # 1 * 80.00

        # Modificar la cantidad del item: de 1 a 5
        order_item.quantity = 5
        order_item.save() # Esto debería disparar la actualización del total de la orden

        self.order.refresh_from_db()
        self.assertEqual(self.order.total_amount, decimal.Decimal('400.00')) # 5 * 80.00

    def test_order_total_amount_update_on_order_item_delete(self):
        """
        Asegura que el total del pedido se actualiza cuando
        un OrderItem es eliminado.
        """
        # Crear varios items
        OrderItem.objects.create(order=self.order, product=self.product_a, quantity=2, price_at_order=self.product_a.price)
        item_to_delete = OrderItem.objects.create(order=self.order, product=self.product_b, quantity=1, price_at_order=self.product_b.price)
        
        self.order.refresh_from_db()
        initial_total = (self.product_a.price * 2) + (self.product_b.price * 1)
        self.assertEqual(self.order.total_amount, initial_total)

        # Eliminar un item
        item_to_delete.delete() # Esto debería disparar el recalculate_total_amount

        self.order.refresh_from_db()
        expected_total_after_delete = (self.product_a.price * 2)
        self.assertEqual(self.order.total_amount, expected_total_after_delete)

    def test_unique_together_constraint(self):
        """
        Asegura que no se puede añadir el mismo producto dos veces al mismo pedido.
        """
        OrderItem.objects.create(
            order=self.order, product=self.product_a, quantity=1, price_at_order=self.product_a.price
        )
        
        # Intentar crear otro OrderItem con la misma orden y producto
        with self.assertRaises(IntegrityError):
            OrderItem.objects.create(
                order=self.order, product=self.product_a, quantity=1, price_at_order=self.product_a.price
            )