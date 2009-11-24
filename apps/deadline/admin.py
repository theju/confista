from django.contrib import admin
from deadline.models import Deadline

class DeadlineAdmin(admin.ModelAdmin):
    pass

admin.site.register(Deadline, DeadlineAdmin)
