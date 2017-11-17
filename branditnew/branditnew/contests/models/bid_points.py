from django.db import models


class Bid_Point(models.Model):
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    name  = models.CharField(max_length=50, ${blank=True, null=True})
    price = models.PositiveSmallIntegerField(blank=True, null=True)


    def __str__(self):
        return self.name

