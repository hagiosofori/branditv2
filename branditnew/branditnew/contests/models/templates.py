from django.db import models
from django.contrib.auth.models import User





class Template_Category(models.Model):
    name = models.CharField(max_length=100)





class Template(models.Model):
    image = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cost = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    




class Template_Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    changes = models.TextField(blank=True, null=True)
    total_cost = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.template.name +' for client @'+ self.client.username
