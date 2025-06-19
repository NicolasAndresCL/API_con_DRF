# customers/views.py
from rest_framework import viewsets
# Importa también 'AllowAny' para permitir acceso sin autenticación
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.exceptions import ValidationError
from .models import Customer
from .serializers import CustomerSerializer

class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # ELIMINA la línea 'permission_classes = [IsAuthenticated, IsAdminUser]' de aquí.
    # Los permisos se gestionarán dinámicamente en el método get_permissions.

    def get_permissions(self):
        """
        Sobrescribe este método para aplicar permisos basados en la acción que se está realizando.
        Esto permite que algunas acciones (como 'list' o 'retrieve') sean públicas,
        mientras que otras (como 'create', 'update', 'destroy') requieran autenticación
        o que el usuario sea administrador.
        """
        # Define las clases de permisos que se aplicarán para la acción actual.
        if self.action == 'list' or self.action == 'retrieve':
            # Para la acción de listar (GET /api/customers/)
            # y la acción de recuperar un cliente específico (GET /api/customers/{id}/)
            # permitimos acceso a CUALQUIER usuario, esté autenticado o no.
            permission_classes = [AllowAny]
        elif self.action == 'create':
            # Para la acción de crear un cliente (POST /api/customers/)
            # solo permitimos a usuarios AUTENTICADOS. Si deseas que solo los admins
            # puedan crear, cambia IsAuthenticated por IsAdminUser.
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            # Para las acciones de actualizar (PUT/PATCH /api/customers/{id}/)
            # y eliminar (DELETE /api/customers/{id}/)
            # solo permitimos a usuarios que sean ADMINISTRADORES.
            permission_classes = [IsAdminUser]
        else:
            # Para cualquier otra acción personalizada que puedas agregar en el futuro,
            # por defecto requerimos que el usuario esté autenticado.
            permission_classes = [IsAuthenticated]

        # Retorna una lista de instancias de las clases de permisos.
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Define el queryset base para todas las acciones de este ViewSet.
        Si la acción es 'list' o 'retrieve' y has configurado 'AllowAny' en get_permissions,
        entonces debes permitir que se muestren todos los clientes.
        Tu lógica actual de 'if self.request.user.is_authenticated:' hace que solo los
        usuarios autenticados vean algo, lo cual contradice 'AllowAny' para 'list'.

        Para que la lista sea visible para todos (cuando se usa AllowAny para 'list'),
        simplemente devuelve todos los objetos Customer. Los permisos (get_permissions)
        se encargarán de restringir las operaciones de escritura.
        """
        # Si la acción es 'list' o 'retrieve' y los permisos ya lo han permitido
        # a cualquier usuario (AllowAny), entonces queremos que se muestren todos los clientes.
        # Si las acciones de creación/actualización/eliminación solo están disponibles para
        # usuarios autenticados/admin, esta función aún devolverá todos los clientes
        # si se intenta hacer una acción de creación/actualización/eliminación *si el usuario es válido*
        # (los permisos lo habrán filtrado antes).
        return Customer.objects.all()

    def perform_create(self, serializer):
        """
        Sobrescribe el método para guardar el objeto cuando se crea.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Sobrescribe el método para definir una lógica personalizada antes de eliminar un cliente.
        En este caso, impide la eliminación si el cliente tiene pedidos pendientes.
        """
        # Verifica si el cliente tiene pedidos con el estado 'pending'.
        # Asume que 'orders' es el related_name de tu ForeignKey en el modelo Order que apunta a Customer.
        # Si no definiste related_name, sería 'order_set'.
        if instance.orders.filter(status='pending').exists():
            # Si hay pedidos pendientes, lanza un error de validación que DRF manejará.
            raise ValidationError(
                {"detail": "No se puede eliminar un cliente con pedidos pendientes."}
            )
        # Si no hay pedidos pendientes, llama al método perform_destroy original para eliminar la instancia.
        super().perform_destroy(instance)
