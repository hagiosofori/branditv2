from django.db import models

class Price(models.Model):
    price_type = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=100000000, decimal_places=2)

    def __str__(self):
        return self.price_type
