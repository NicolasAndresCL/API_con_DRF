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
    path('api/', include("orders.urls")),  
    path('api/', include("products.urls")), 

    # Endpoint para obtener un token (requiere POST con username y password)
    path('api/token/', authtoken_views.obtain_auth_token, name='obtain_token'),

    # URLs para OpenAPI y documentación (drf-spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('', RedirectView.as_view(url='api/schema/swagger-ui/', permanent=False), name='index_to_swagger'),
    # ---------------------------------------------------------------------------------
]