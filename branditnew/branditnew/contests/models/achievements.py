from django.db import models
from django.contrib.auth.models import User

from branditnew.contests.models.entries import Entry



class Modes_of_Payment(models.Model):
    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name


class Achievement(models.Model):
    brandlancer = models.ForeignKey(User, on_delete=models.CASCADE)
    winning_entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    prize_amount = models.PositiveSmallIntegerField()
    mode_of_payment = models.ForeignKey(Modes_of_Payment, on_delete=models.CASCADE, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    payment_token = models.CharField(max_length=50, blank=True, null=True)
    requested = models.BooleanField(default=False)
    payment_details = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.winning_entry.title + ' by '+self.brandlancer.username
    