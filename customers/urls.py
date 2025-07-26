# customers/urls.py
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from customers.views import CustomerView
from customers.schema_auth import DecoratedTokenObtainPairView

router = SimpleRouter()
router.register(r"customers", CustomerView, basename="customers")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", DecoratedTokenObtainPairView.as_view(), name="token_obtain_pair"),
]
