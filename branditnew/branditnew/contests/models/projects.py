from django.db import models
from django.contrib.auth.models import User


def project_submissions_directory_path(instance, filename):
    return 'project_{0}/{1}'.format(instance.project.id, filename)



class Project(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    is_complete = models.BooleanField(default=False)



class Project_Submission(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    submission = models.FileField(upload_to=project_submissions_directory_path)
    is_approved = models.BooleanField(default=False)



class Project_Submission_Comment(models.Model):
    project_submission = models.ForeignKey(Project_Submission, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
