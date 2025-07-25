from django.urls import path, include
from rest_framework.routers import SimpleRouter
from orders.views import OrderViewSet

router = SimpleRouter()
router.register(r"orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
]
