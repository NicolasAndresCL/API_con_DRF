from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=["Autenticación"],
    summary="Obtener token de autenticación",
    description="Recibe username y password, y retorna un token para autenticación.",
    request={"application/json": {"username": "usuario", "password": "contraseña"}},
    responses={200: {"token": "abc123xyz"}}
)
@api_view(["POST"])
@permission_classes([AllowAny])
def decorated_obtain_auth_token(request):
    return obtain_auth_token(request)
