from django.urls import path
from .views import ProductsView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"products", ProductsView, basename="product")

urlpatterns = router.urls