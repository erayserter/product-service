import re
from _decimal import Decimal

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)

from product.models import Product
from product.serializers import ProductSerializer

from shopping.permissions import IsOwner


class RetrieveProductAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'code'


class ListProductAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProductSerializer
    search_fields = ["name", "code", "brand", ]

    def get_queryset(self):  # TODO: will be fixed
        queryset = Product.objects.all()

        name = self.request.query_params.get('name')
        code = self.request.query_params.get('code')
        brand = self.request.query_params.get('brand')
        price_interval = self.request.query_params.get('price_interval')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if code:
            queryset = queryset.filter(code__exact=code)
        if brand:
            queryset = queryset.filter(brand__exact=brand)
        if price_interval and re.match("^\\d+-\\d+$", price_interval):
            prices = price_interval.split('-')
            queryset = queryset.filter(price__gte=prices[0], price__lte=prices[1])

        return queryset


class CreateProductAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UpdateProductAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwner, ]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'code'


class DestroyProductAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner, ]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'code'
