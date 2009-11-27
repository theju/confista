from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<id>\d+)/$', "talk.views.list",     name="talk_list_id"),
    url(r'^all/$',         "talk.views.list",     name="talk_list_all"),
    url(r'^add/$',         "talk.views.add_talk", name="talk_add_talk"),
    url(r'^feed/$',        "talk.views.feed_all", name="talk_feed_all"),
)
