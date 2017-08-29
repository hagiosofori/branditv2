# entries fields

# : contest [foreign key]

# : brandlancer [foreign key]

# : files url

# : message

# : sub

# : boost

# : hide

# : cost

# : date created

# : likes

# : is_winner

from django.db import models
from .contest import Contest
from django.contrib.auth.models import User

class Entry(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)  
    brandlancer = models.ForeignKey(User, on_delete=models.CASCADE)
    files = models.FileField(upload_to='uploads/') #url to the storage folder
    message = models.TextField(null=True) 
    sub = models.NullBooleanField() 
    boost = models.NullBooleanField() 
    hide = models.NullBooleanField() 
    cost = models.DecimalField(max_digits=10000000, decimal_places=2, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    number_of_likes = models.DecimalField(max_digits=10000000, decimal_places=0, default=0)
    is_winner = models.BooleanField(default=False)
