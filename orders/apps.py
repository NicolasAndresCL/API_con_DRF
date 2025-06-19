from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self):
        # Importar las señales aquí para que se conecten cuando la app esté lista
        import orders.signals 