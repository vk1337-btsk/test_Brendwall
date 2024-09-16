from django.core.exceptions import ValidationError
from django.db import models


class Product(models.Model):
    """Модель для отображения продукта."""

    name = models.CharField(max_length=100, blank=True, verbose_name="Название продукта")
    description = models.TextField(blank=True, verbose_name="Описание продукта")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость продукта")

    def __str__(self):
        return f"{self.name} - {self.price}"
