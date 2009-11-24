from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^all/$', "statistics.views.list_all", name="statistics_list_all"),
)
