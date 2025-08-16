
from rest_framework import viewsets, filters, status
from .models import Order, OrderItem
from core.models import Product
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from core.views import RegisterView
from core.serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCustomerOwner, IsSellerOrAdmin
from core.models import PlatformApiCall
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Prefetch

# Mixin to log API calls per-view (in addition to middleware)
class PlatformApiCallMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        try:
            PlatformApiCall.objects.create(
                user = request.user if request.user.is_authenticated else None,
                requested_url = request.get_full_path(),
                requested_data = request.data if hasattr(request,'data') else None,
                response_data = getattr(response, 'data', None)
            )
        except Exception:
            pass
        return super().finalize_response(request, response, *args, **kwargs)

class ProductViewSet(PlatformApiCallMixin, viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_deleted=False).order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['amount','name']

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class OrderViewSet(PlatformApiCallMixin, viewsets.ModelViewSet):
    queryset = Order.objects.filter(is_deleted=False).select_related('customer__user','seller__user').prefetch_related(Prefetch('items__product'))
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer__id','seller__id']
    search_fields = ['items__product__name']
    ordering_fields = ['amount','created_at']

    def get_permissions(self):
        # Customers can only view their own
        if self.action in ['list','retrieve']:
            return [IsAuthenticated(), IsCustomerOwner()]
        return [IsAuthenticated(), IsSellerOrAdmin()]

    def list(self, request, *args, **kwargs):
        # Support top5 via ?top=5 and sorting via ordering
        top = request.query_params.get('top')
        if top:
            qs = self.filter_queryset(self.get_queryset()).order_by('-amount')[:int(top)]
            page = self.paginate_queryset(qs)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)
