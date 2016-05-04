from django.contrib import admin

from .models import *

admin.site.register(Project)
admin.site.register(ProjectGroup)
admin.site.register(Proposal)
admin.site.register(Completion)
