from django.db import models
from django.contrib.auth.models import User

from branditnew.contests.models.achievements import Modes_of_Payment


class Payment_Request(models.Model):
    brandlancer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mode_of_payment = models.ForeignKey(Modes_of_Payment, on_delete=models.SET_NULL, blank=True, null=True)
    payment_details = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
