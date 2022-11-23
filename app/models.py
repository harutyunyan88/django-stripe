from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField()


class Cart(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
