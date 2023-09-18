from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    owner = ReadOnlyField(source='owner.username')

    class Meta:
        model = Product
        fields = ('code', "owner", "name", "brand", "description", "price", "price_unit", "stock", "has_stock", )
        read_only_fields = ('owner', )
        lookup_field = 'code'
