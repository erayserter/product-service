from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    CURRENCY_CHOICES = (
        ("TRY", "Turkish Lira"),
        ("GBP", "Sterling"),
        ("USD", "United States Dollar"),
        ("EUR", "Euro"),
    )

    owner = ReadOnlyField(source='owner.username')
    price_unit = serializers.ChoiceField(choices=CURRENCY_CHOICES, default=CURRENCY_CHOICES[0])

    class Meta:
        model = Product
        fields = ('code', "owner", "name", "brand", "description", "price", "price_unit", "stock", "has_stock", )
        read_only_fields = ('owner', )
        lookup_field = 'code'
