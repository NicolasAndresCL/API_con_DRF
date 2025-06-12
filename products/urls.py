from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"products", views.ProductViewSet, "products") # 'products' será el basename

urlpatterns = [
    path("", include(router.urls)), # No prefix here, will be handled by the project's urls.py
]