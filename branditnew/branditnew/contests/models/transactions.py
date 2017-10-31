from django.db import models
from django.contrib.auth.models import User



class Transaction_Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Transaction_Status(models.Model):
    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name



class Transaction(models.Model):
    client = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Transaction_Type, on_delete=models.DO_NOTHING)
    amount = models.PositiveSmallIntegerField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type + ' by ' + self.client.username + ' on ' + self.created_at 