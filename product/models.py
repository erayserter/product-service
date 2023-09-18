import uuid

from django.db import models
from django.contrib.auth.models import User

from shopping.models import BaseModel, BaseModelManager


class Product(BaseModel):
    name = models.CharField(max_length=127)
    code = models.UUIDField(default=uuid.uuid4, unique=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    description = models.CharField(max_length=511)
    brand = models.CharField(max_length=127)
    price_unit = models.CharField(max_length=7)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    objects = BaseModelManager()

    @property
    def has_stock(self):
        return self.stock > 0
