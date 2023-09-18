import re

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from product.models import Product
from product.serializers import ProductSerializer

from shopping.permissions import IsOwnerOrReadOnly


class RetrieveUpdateDestroyProductAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, ]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'code'


class ListCreateProductAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
