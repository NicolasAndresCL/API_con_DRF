from django.urls import path, include
from rest_framework.routers import DefaultRouter
from customers import views

router = DefaultRouter()
router.register(r"customers", views.CustomerView, "customers")

urlpatterns = [
    path("", include(router.urls)),
]