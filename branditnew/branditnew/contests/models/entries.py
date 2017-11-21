from django.db import models
from .contest import Contest
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.brandlancer.id, filename)

class Entry(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    brandlancer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=True, null=True)
    files = models.FileField(upload_to=user_directory_path, blank=True,null=True)
    message = models.TextField(null=True)
    sub = models.BooleanField(default=False)
    boost = models.BooleanField(default=False)
    hide = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=10000000, decimal_places=2, null=True, default=0)
    payment_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    number_of_likes = models.DecimalField(max_digits=10000000, decimal_places=0, default=0)
    is_winner = models.BooleanField(default=False)

    

    def __str__(self):
        return self.title





class Entry_Comment(models.Model):
    contest_entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    is_touched = models.BooleanField(default=False)

    def __str__(self):
        return self.content

    def touch(self):
        self.is_touched = True



def get_num_new_contest_entry_comments():
    return Entry_Comment.objects.filter(is_touched=False).count()


