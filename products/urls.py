from django.urls import path, include
from rest_framework.routers import SimpleRouter
from products.views import ProductViewSet

router = SimpleRouter()
router.register(r"products", ProductViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
]
