from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', "schedule.views.display_schedule", name="display_schedule"),
    url(r'^/day/(?P<day>\d+)/hall/(?P<hall>\d+)/$', 
        'schedule.views.display_schedule_by_hall', 
        name='display_schedule_by_hall'),
)
