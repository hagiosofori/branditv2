from . import skills
from . import profiles
from . import categories
from . import contest
from . import entries
from . import forms
from . import prices
from . import projects
from . import templates
from . import print_orders


def touch(obj):
    obj.is_touched = True
