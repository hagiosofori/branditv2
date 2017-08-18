from django.contrib import admin

from .models import categories
from .models import contest
from .models import profiles
from .models import skills
from .models import user_type

# Register your models here.
class ProfilesAdmin(admin.ModelAdmin):
    fields = 