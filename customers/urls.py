from django.urls import path, include
from rest_framework.routers import SimpleRouter 
from customers.views import CustomerView
from .schema_auth import decorated_obtain_auth_token

router = SimpleRouter()
router.register(r"customers", CustomerView, basename="customers")

urlpatterns = [
    path("token/", decorated_obtain_auth_token, name="obtain_token"),
    path("", include(router.urls)),
]
