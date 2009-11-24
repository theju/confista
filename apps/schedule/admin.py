from django.contrib import admin
from schedule.forms import SlotForm
from schedule.models import Day, Hall, Slot

class ScheduleAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        return SlotForm

admin.site.register(Day)
admin.site.register(Hall)
admin.site.register(Slot, ScheduleAdmin)
