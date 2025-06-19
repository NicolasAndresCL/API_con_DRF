import decimal # Para trabajar con DecimalField de forma precisa
from django.test import TestCase
from django.utils import timezone # Aunque auto_now_add/auto_now lo manejan, es bueno saberlo
import time # Para manejar el tiempo de creación y actualización

from .models import Product

class ProductModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Product.
    """

    def setUp(self):
        """
        Configuración que se ejecuta ANTES de cada método de prueba.
        Aquí creamos una instancia básica de Product para cada test.
        """
        self.product = Product.objects.create(
            name='Smartphone X',
            description='Un teléfono inteligente de última generación.',
            price=decimal.Decimal('799.99'),
            stock=50,
            is_active=True
        )

        time.sleep(0.001)

    # --- Pruebas de Creación y Atributos Básicos ---
    def test_product_creation(self):
        """Asegura que un Product se puede crear correctamente."""
        self.assertIsInstance(self.product, Product) # Verifica que es una instancia de Product
        self.assertEqual(self.product.name, 'Smartphone X') # Verifica el nombre
        self.assertEqual(self.product.description, 'Un teléfono inteligente de última generación.') # Verifica la descripción
        self.assertEqual(self.product.price, decimal.Decimal('799.99')) # Verifica el precio
        self.assertEqual(self.product.stock, 50) # Verifica el stock
        self.assertTrue(self.product.is_active) # Verifica que está activo

        # Los campos auto_now_add y auto_now
        self.assertIsNotNone(self.product.created_at) # Verifica que created_at no es nulo
        self.assertIsNotNone(self.product.updated_at) # Verifica que updated_at no es nulo
        # Opcional: Puedes verificar que created_at es anterior o igual a updated_at
        self.assertLessEqual(self.product.created_at, self.product.updated_at)


    def test_product_str_representation(self):
        """Asegura que el método __str__ de Product devuelve el nombre del producto."""
        self.assertEqual(str(self.product), 'Smartphone X')

    # --- Pruebas de Campos Numéricos y Valores Por Defecto ---
    def test_product_default_values(self):
        """
        Prueba que los valores por defecto (stock, is_active) se aplican correctamente
        cuando no se especifican.
        """
        product_default = Product.objects.create(
            name='Auriculares',
            price=decimal.Decimal('99.99')
            # No especificamos description, stock, is_active
        )
        self.assertEqual(product_default.stock, 0) # Valor por defecto de stock
        self.assertTrue(product_default.is_active) # Valor por defecto de is_active
        self.assertIsNone(product_default.description) # Valor por defecto de description (null=True, blank=True)

    def test_price_decimal_places(self):
        """Asegura que el campo price maneja correctamente los decimales."""
        product_decimal = Product.objects.create(
            name='Artículo con centavos',
            price=decimal.Decimal('1.23'),
            stock=1
        )
        self.assertEqual(product_decimal.price, decimal.Decimal('1.23'))

        product_no_decimal = Product.objects.create(
            name='Artículo sin centavos',
            price=decimal.Decimal('50.00'),
            stock=1
        )
        self.assertEqual(product_no_decimal.price, decimal.Decimal('50.00'))

    def test_negative_stock(self):
        """
        Aunque Django no lo prohíbe por defecto para IntegerField,
        es una buena práctica probar y documentar que tu lógica de negocio
        debería prevenir stocks negativos (posiblemente con validadores o en formularios/serializers).
        Aquí solo probamos que el modelo *puede* almacenarlo si no hay validación adicional.
        """
        product_negative_stock = Product.objects.create(
            name='Producto en Negativo',
            price=decimal.Decimal('10.00'),
            stock=-5 # Django permite esto a nivel de modelo por defecto
        )
        self.assertEqual(product_negative_stock.stock, -5)
        # Si quisieras prohibir esto a nivel de modelo, necesitarías un validador personalizado
        # y luego probarías que lanzar un ValidationError.

    # --- Pruebas de Actualización de Campos ---
    def test_product_update(self):
        """Asegura que los campos de un producto pueden ser actualizados."""
        old_updated_at = self.product.updated_at # Guarda el valor original de updated_at

        time.sleep(0.001) # Espera un poco para asegurar que updated_at cambia
        
        # Modifica el producto
        self.product.name = 'Smartphone Y'
        self.product.price = decimal.Decimal('850.00')
        self.product.stock = 45
        self.product.is_active = False
        self.product.save() # Guarda los cambios en la base de datos

        # Recarga el producto desde la DB para asegurar que los cambios se persistieron
        self.product.refresh_from_db() 

        # Verifica los cambios
        self.assertEqual(self.product.name, 'Smartphone Y')
        self.assertEqual(self.product.price, decimal.Decimal('850.00'))
        self.assertEqual(self.product.stock, 45)
        self.assertFalse(self.product.is_active)
        
        # Verifica que updated_at se actualizó (debe ser mayor que el valor original)
        self.assertGreater(self.product.updated_at, old_updated_at) 


    def test_product_delete(self):
        """Asegura que un producto puede ser eliminado."""
        product_to_delete = Product.objects.create(
            name='Producto para borrar',
            price=decimal.Decimal('1.00'),
            stock=1
        )
        
        # Verificar que el producto existe antes de borrar
        self.assertTrue(Product.objects.filter(id=product_to_delete.id).exists())

        product_to_delete.delete()

        # Verificar que el producto ya no existe
        self.assertFalse(Product.objects.filter(id=product_to_delete.id).exists())
        self.assertEqual(Product.objects.count(), 1) # Solo queda el self.product del setUp