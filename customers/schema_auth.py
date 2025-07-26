from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiExample
from rest_framework.permissions import AllowAny

@extend_schema_view(
    post=extend_schema(
        tags=["Autenticación"],
        summary="Obtener access y refresh token (JWT)",
        description="Autenticación vía JWT. Requiere username y password válidos.",
        request=TokenObtainPairSerializer,
        responses={200: None},
        examples=[
            OpenApiExample(
                name="Login ejemplo",
                request_only=True,
                value={"username": "admin", "password": "admin123"},
            )
        ],
    )
)
class DecoratedTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
# customers/services/tasks.py
from customers.services.tasks import task_saludo_desde_celery

def lanzar_saludo():
    return task_saludo_desde_celery.delay()

