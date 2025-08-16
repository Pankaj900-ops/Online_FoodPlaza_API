
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, ProductViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]
