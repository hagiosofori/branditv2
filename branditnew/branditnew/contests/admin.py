from django.contrib import admin

from .models import categories
from .models import contest
from .models import profiles
from .models import skills
from .models import user_type
from .models import entries
from .models import prices
from .models import projects

# Register your models here.
class ProfilesAdmin(admin.ModelAdmin):
    fields = [
        'user_name', 
        'user_type', 
        'phone_number', 
        'activation_key', 
        'is_activated', 
        'points', 
        'skills', 
        'profile_image', 
        'address', 
        'bio', 
        'date_of_birth', 
        'how_found_us',
    ]

admin.site.register(profiles.Profile, ProfilesAdmin)
admin.site.register(skills.Skill)
admin.site.register(user_type.User_type)
admin.site.register(contest.Contest)
admin.site.register(categories.Category)
admin.site.register(entries.Entry)
admin.site.register(prices.Price)
admin.site.register(projects.Project)
admin.site.register(projects.Project_Submission)
admin.site.register(projects.Project_Submission_Comment)
admin.site.register(entries.Entry_Comment)
