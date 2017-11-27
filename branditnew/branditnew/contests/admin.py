from django.contrib import admin

from .models import categories
from .models import contest
from .models import profiles
from .models import skills
from .models import user_type
from .models import entries
from .models import prices
from .models import projects
from .models import templates
from .models import transactions
from .models import print_orders
from .models import bid_points
from .models import achievements
from .models import payment_requests

# Register your models here.
admin.site.register(profiles.Profile)
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
admin.site.register(templates.Template)
admin.site.register(templates.Template_Order)
admin.site.register(templates.Template_Category)
admin.site.register(transactions.Transaction)
admin.site.register(transactions.Transaction_Type)
admin.site.register(transactions.Transaction_Status)
admin.site.register(print_orders.Item)
admin.site.register(print_orders.Print_Order)
admin.site.register(bid_points.Bid_Point)
admin.site.register(bid_points.Points_Purchase)
admin.site.register(achievements.Achievement)
admin.site.register(achievements.Modes_of_Payment)
admin.site.register(payment_requests.Payment_Request)
