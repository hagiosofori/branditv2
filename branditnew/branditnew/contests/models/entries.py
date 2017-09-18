from django.db import models
from .contest import Contest
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Entry(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    brandlancer = models.ForeignKey(User, on_delete=models.CASCADE)
    files = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    message = models.TextField(null=True)
    sub = models.BooleanField(default=False)
    boost = models.BooleanField(default=False)
    hide = models.BooleanField(default=False)
    cost = models.DecimalField(
        max_digits=10000000, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    number_of_likes = models.DecimalField(
        max_digits=10000000, decimal_places=0, default=0)
    is_winner = models.BooleanField(default=False)

    # def __str__(self):
    #     self.message


