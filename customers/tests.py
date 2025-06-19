from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError # Para probar validaciones de modelos
from django.db.utils import IntegrityError # Para probar restricciones de unicidad (email)

import datetime # Para trabajar con objetos de fecha
import time # Para el sleep en updated_at

from .models import Customer

class CustomerModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Customer.
    """

    def setUp(self):
        """
        Configuración que se ejecuta ANTES de cada método de prueba.
        Crea una instancia básica de Customer para cada test.
        """
        self.customer_data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice.smith@example.com',
            'phone_number': '987654321',
            'date_of_birth': datetime.date(1990, 5, 15),
            'address_line_1': '123 Main St',
            'city': 'Santiago',
            'state_province': 'Region Metropolitana',
            'postal_code': '8320000',
            'country': 'Chile',
            'is_active': True,
            'notes': 'Cliente regular y amigable.'
        }
        self.customer = Customer.objects.create(**self.customer_data)

    # --- Pruebas de Creación y Atributos Básicos ---
    def test_customer_creation(self):
        """Asegura que un Customer se puede crear correctamente con todos los campos."""
        self.assertIsInstance(self.customer, Customer)
        self.assertEqual(self.customer.first_name, 'Alice')
        self.assertEqual(self.customer.last_name, 'Smith')
        self.assertEqual(self.customer.email, 'alice.smith@example.com')
        self.assertEqual(self.customer.phone_number, '987654321')
        self.assertEqual(self.customer.date_of_birth, datetime.date(1990, 5, 15))
        self.assertEqual(self.customer.address_line_1, '123 Main St')
        self.assertEqual(self.customer.city, 'Santiago')
        self.assertEqual(self.customer.state_province, 'Region Metropolitana')
        self.assertEqual(self.customer.postal_code, '8320000')
        self.assertEqual(self.customer.country, 'Chile')
        self.assertTrue(self.customer.is_active)
        self.assertIsNotNone(self.customer.date_joined) # default=timezone.now
        self.assertIsNotNone(self.customer.last_updated) # auto_now=True
        self.assertEqual(self.customer.notes, 'Cliente regular y amigable.')
        # created_at debe ser <= last_updated
        self.assertLessEqual(self.customer.date_joined, self.customer.last_updated)


    def test_customer_str_representation(self):
        """Asegura que el método __str__ de Customer devuelve el string esperado."""
        expected_str = "Alice Smith (alice.smith@example.com)"
        self.assertEqual(str(self.customer), expected_str)

    def test_full_name_property(self):
        """Prueba la propiedad 'full_name'."""
        self.assertEqual(self.customer.full_name, "Alice Smith")

    def test_full_address_property(self):
        """Prueba la propiedad 'full_address' con y sin address_line_2."""
        expected_address = "123 Main St, Santiago, Region Metropolitana 8320000, Chile"
        self.assertEqual(self.customer.full_address, expected_address)

        # Prueba sin address_line_2
        customer_no_address2 = Customer.objects.create(
            first_name='Bob',
            last_name='Brown',
            email='bob.brown@example.com',
            address_line_1='456 Oak Ave',
            city='Valparaiso',
            state_province='Valparaiso',
            postal_code='2340000'
        )
        expected_address_no_address2 = "456 Oak Ave, Valparaiso, Valparaiso 2340000, Chile"
        self.assertEqual(customer_no_address2.full_address, expected_address_no_address2)

    # --- Pruebas de Campos Opcionales y Valores Por Defecto ---
    def test_customer_default_values(self):
        """
        Prueba que los valores por defecto (is_active, country, date_joined)
        y campos nulos (phone_number, date_of_birth, etc.) funcionan.
        """
        customer_defaults = Customer.objects.create(
            first_name='Charlie',
            last_name='Davies',
            email='charlie.davies@example.com'
        )
        self.assertTrue(customer_defaults.is_active) # Default
        self.assertEqual(customer_defaults.country, 'Chile') # Default
        self.assertIsNotNone(customer_defaults.date_joined) # Default

        self.assertIsNone(customer_defaults.phone_number) # Nullable
        self.assertIsNone(customer_defaults.date_of_birth) # Nullable
        self.assertIsNone(customer_defaults.address_line_1) # Nullable
        # ... y así sucesivamente para todos los campos blank=True, null=True

    # --- Pruebas de Validaciones y Restricciones ---
    def test_unique_email_constraint(self):
        """Asegura que no se puede crear un cliente con un email ya existente."""
        # Un cliente con 'alice.smith@example.com' ya existe del setUp
        
        with self.assertRaises(IntegrityError):
            Customer.objects.create(
                first_name='Another',
                last_name='User',
                email='alice.smith@example.com' # Email duplicado
            )
        # Nota: La `IntegrityError` se dispara a nivel de base de datos.
        # Si quieres validar esto antes de intentar guardar en la DB,
        # necesitarías usar `full_clean()` o validaciones a nivel de formulario/serializer.
        # Por ahora, probar la IntegrityError es suficiente para el modelo.

    def test_email_field_validation(self):
        """
        Asegura que el campo email valida formatos básicos de email.
        Django's EmailField tiene validación incorporada en full_clean().
        """
        invalid_emails = [
            'invalid-email',
            'user@.com',
            'user@com',
            'user@domain'
        ]
        for invalid_email in invalid_emails:
            with self.assertRaises(ValidationError):
                customer = Customer(
                    first_name='Test',
                    last_name='Email',
                    email=invalid_email
                )
                customer.full_clean() # Fuerza la validación de Django
    
    def test_charfield_max_length(self):
        """Asegura que los CharField respetan su max_length."""
        with self.assertRaises(ValidationError):
            customer = Customer(
                first_name='A' * 101, # Excede max_length=100
                last_name='Test',
                email='test@example.com'
            )
            customer.full_clean()


    # --- Pruebas de Actualización de Campos ---
    def test_customer_update(self):
        """Asegura que los campos de un cliente pueden ser actualizados."""
        old_last_updated = self.customer.last_updated
        time.sleep(0.001) # Pequeña pausa para asegurar que last_updated cambie

        self.customer.first_name = 'Alicia'
        self.customer.phone_number = '111222333'
        self.customer.is_active = False
        self.customer.save()

        self.customer.refresh_from_db()

        self.assertEqual(self.customer.first_name, 'Alicia')
        self.assertEqual(self.customer.phone_number, '111222333')
        self.assertFalse(self.customer.is_active)
        self.assertGreater(self.customer.last_updated, old_last_updated) # last_updated debe ser mayor

    def test_customer_delete(self):
        """Asegura que un cliente puede ser eliminado."""
        customer_to_delete = Customer.objects.create(
            first_name='Delete', last_name='Me', email='delete.me@example.com'
        )
        self.assertTrue(Customer.objects.filter(id=customer_to_delete.id).exists())

        customer_to_delete.delete()

        self.assertFalse(Customer.objects.filter(id=customer_to_delete.id).exists())
        self.assertEqual(Customer.objects.count(), 1) # Solo queda el self.customer del setUp