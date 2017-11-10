from datetime import datetime

from django.db import models
from django.contrib.auth.models import User



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/print_order{1}/{2}'.format(instance.client.id,instance.id, filename)



def item_image_path(instance, filename):
    return 'item{0}_{1}'.format(instance.name, filename)



class Item(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    image = models.FileField(upload_to=item_image_path, blank=True, null=True)
    price = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name





class Print_Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True)
    uploaded_design = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    cost = models.PositiveSmallIntegerField(blank=True, null=True)

    is_paid = models.BooleanField(default=False)
    is_touched = models.BooleanField(default=False)
    #created_at

    def __str__(self):
        return "{0}'s print order for {2} {1}s".format(self.client, self.item, self.quantity)

