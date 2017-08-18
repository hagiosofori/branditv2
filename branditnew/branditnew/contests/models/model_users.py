from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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



    user = models.OneToOneField(User,
    on_delete=models.CASCADE)     #using django's built-in user class, along with our extra fields in this class
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=6, default=CLIENT, blank=False, null=False) #usertype, either admin, client or brandlancer
    telephone = models.CharField #user's telephone number
    activation_key = models.CharField(max_length=50)
    is_activated = models.BooleanField(default=False) #value representing whether the account is activated or not
    points = models.DecimalField(max_digits=10000, decimal_places=0)
    skills = models.ForeignKey('Skills', on_delete='SET_NULL')
    profile_image = models.ImageField(upload_to='uploads/profile_images/%Y/%m/%d')
    address = models.CharField(max_length=50)
    bio = models.TextField()
    date_of_birth = models.DateField()
    how_found_us = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    
    def __str__(self):
        return self.user.get_full_name()
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
       Profile.objects.create(user=instance)
     
    
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.Profile.save()
