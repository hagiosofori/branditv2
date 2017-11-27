from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from . import skills

class Skills(models.Model):
    class Meta:
        app_label = 'contests'


    SKILLS_CHOICES = [
        ['php', 'PHP'],
        ['css', 'CSS'],
        ['html', 'HTML'],
        ['photoshop', 'Photoshop'],
        ['coralDraw', 'Coral Draw'],
    ]

    name = models.CharField(max_length=100, choices=SKILLS_CHOICES, blank=False, null=False)




class Profile(models.Model):
    class Meta:
        app_label = 'contests'

    #options for user type
    ADMIN = 'admin'
    CLIENT = 'client'
    BRANDLANCER = 'bl'

    USER_TYPE_CHOICES = [
        [ADMIN, 'Administrator'],
        [CLIENT, 'Client'],
        [BRANDLANCER, 'Brandlancer'],
    ]



    user = models.OneToOneField(User, on_delete=models.CASCADE)     #using django's built-in user class, along with our extra fields in this class
    user_name = models.CharField(max_length=50, null=True, blank=True)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=6, default=CLIENT, blank=False, null=True) #usertype, either admin, client or brandlancer
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") #validation for international phone numbers
    phone_number = models.CharField(validators=[phone_regex], null=True, blank=True, max_length=15) #user's telephone number
    activation_key = models.CharField(max_length=50, null=True, blank=True)
    is_activated = models.NullBooleanField(default=False, null=True, blank=True) #value representing whether the account is activated or not
    points = models.DecimalField(max_digits=10000, decimal_places=0, null=True, blank=True)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    skills = models.ForeignKey(Skills, on_delete=models.DO_NOTHING, null=True, blank=True)
    profile_image = models.FileField(upload_to='uploads/profile_images/%Y/%m/%d', null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    how_found_us = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    
    def __str__(self):
        return self.user_name
    
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.user_name = instance.username
    instance.profile.save()
