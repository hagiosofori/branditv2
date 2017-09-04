from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50) #the name of the category
    prize_lower_limit = models.PositiveSmallIntegerField() #the least possible cost for a contest in this category
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
