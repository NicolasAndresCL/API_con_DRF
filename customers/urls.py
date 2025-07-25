from django.urls import path, include
from rest_framework.routers import SimpleRouter 
from customers.views import CustomerView

router = SimpleRouter()
router.register(r"customers", CustomerView, basename="customers")

urlpatterns = [
    path("", include(router.urls)),
]
