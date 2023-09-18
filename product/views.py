import re

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
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

    def get_queryset(self):
        queryset = Product.objects.all()

        username = self.kwargs.get('username')
        if username:
            queryset = queryset.filter(owner__username=username)

        name = self.request.query_params.get('name')
        code = self.request.query_params.get('code')
        brand = self.request.query_params.get('brand')
        price_interval = self.request.query_params.get('price_interval')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if code:
            queryset = queryset.filter(code__icontains=code)  # TODO: exact daha mantıklı olabilir.
        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        if price_interval and re.match("^([0-9]*[.])?[0-9]+-([0-9]*[.])?[0-9]+$", price_interval):
            # if matches a string with two floating numbers seperated by -
            prices = price_interval.split('-')
            queryset = queryset.filter(price__gte=prices[0], price__lte=prices[1])

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
