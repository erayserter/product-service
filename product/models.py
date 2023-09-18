import uuid

from django.db import models
from user.models import User

from shopping.models import BaseModel, BaseModelManager


class Product(BaseModel):
    name = models.CharField(max_length=127)
    code = models.CharField(max_length=255, default=uuid.uuid4, unique=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    description = models.CharField(max_length=511)
    brand = models.CharField(max_length=127)
    price_unit = models.CharField(max_length=3)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    objects = BaseModelManager()

    def __str__(self):
        return self.name

    @property
    def has_stock(self):
        return self.stock > 0
