# customers/apps.py
from django.apps import AppConfig

class CustomersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "customers"

    def ready(self):
        from customers.schema_auth import decorated_obtain_auth_token
        from drf_spectacular.openapi import AutoSchema

        decorated_obtain_auth_token.schema = AutoSchema()
