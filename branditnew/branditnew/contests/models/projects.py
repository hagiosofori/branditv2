from django.db import models
from django.contrib.auth.models import User
from branditnew.contests.models.categories import Category
from datetime import datetime

def project_submissions_directory_path(instance, filename):
    return 'project_{0}/submissions/{1}'.format(instance.project.id, filename)



def project_directory_path(instance, filename):
    return 'project_{0}/{1}'.format(instance.id, filename)



class Project(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)
    end_date = models.DateField(default=datetime.today)
    is_draft = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    files = models.FileField(upload_to=project_directory_path, blank=True, null=True)
    cost = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=False)

    def __str__(self):
        return self.title



class Project_Submission(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    submission = models.FileField(upload_to=project_submissions_directory_path)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    



class Project_Submission_Comment(models.Model):
    project_submission = models.ForeignKey(Project_Submission, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content