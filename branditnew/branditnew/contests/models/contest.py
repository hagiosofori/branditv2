from django.db import models
from . import contest
from . import categories
import datetime
from django.contrib.auth.models import User


class Contest(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE) #the client who creates the contest
    title = models.CharField(max_length=50) #the title of the contest
    about = models.TextField() #more detailed information on the contest
    prize = models.PositiveIntegerField() #the prize brandlancer gets for winning the contest for the contest
    end_date = models.DateField(default=datetime.date.today) #the end date of the contest
    is_verified = models.BooleanField(default=False)
    is_paid_for = models.BooleanField(default=False) #whether the client has paid for the contest
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True) #category to which the contest belongs
    is_top = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    is_nda = models.BooleanField(default=False)
    is_sealed = models.BooleanField(default=False)
    cost = models.PositiveSmallIntegerField(blank=True, null=True) #the cost for the contest
    files = models.FileField(upload_to='uploads/%Y/%m/%d/') #files associated with contest
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    preferred_style = models.TextField(blank=True, null=True)
    preferred_colors = models.CharField(max_length=50, blank=True, null=True)
    target_audience = models.TextField(blank=True, null=True)
    design_details = models.TextField(blank=True, null=True)
    would_like_to_print = models.BooleanField()
    logo = models.FileField(upload_to='', blank=True, null=True)
    sketch = models.FileField(upload_to='', blank=True, null=True)

    def __str__(self):
        return self.title
