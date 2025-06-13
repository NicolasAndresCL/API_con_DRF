from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.authtoken import views as authtoken_views # Importa las vistas de authtoken
# Importa RedirectView para poder redirigir la URL raíz
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # URLs de las apps bajo un prefijo '/api/'
    path('api/', include("customers.urls")),
    path('api/', include("products.urls")), 

    # Endpoint para obtener un token (requiere POST con username y password)
    path('api/token/', authtoken_views.obtain_auth_token, name='obtain_token'),

    # URLs para OpenAPI y documentación (drf-spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # ---------------------------------------------------------------------------------
    # NUEVA RUTA PARA REDIRIGIR EL ACCESO A LA RAÍZ AL SWAGGER UI
    # Cuando alguien acceda a http://localhost:8000/ (la ruta vacía ''),
    # será redirigido a http://localhost:8000/api/schema/swagger-ui/. Esto evitara error 404.
    # 'permanent=False' indica una redirección temporal (código 302), ideal para desarrollo.
    # Si fuera para producción, podrías usar 'permanent=True' (código 301).
    path('', RedirectView.as_view(url='api/schema/swagger-ui/', permanent=False), name='index_to_swagger'),
    # ---------------------------------------------------------------------------------
]