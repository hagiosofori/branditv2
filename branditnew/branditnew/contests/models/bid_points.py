from django.db import models
from django.contrib.auth.models import User

class Bid_Point(models.Model):
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    name  = models.CharField(max_length=50, blank=True, null=True)
    price = models.PositiveSmallIntegerField(blank=True, null=True)


    def __str__(self):
        return self.name



class Points_Purchase(models.Model):
    points = models.ForeignKey(Bid_Point, blank=True, null=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    token = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
