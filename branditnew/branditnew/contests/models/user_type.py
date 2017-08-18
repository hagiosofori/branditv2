from django.db import models

class User_type(models.Model):
    name = models.CharField(max_length=50)
