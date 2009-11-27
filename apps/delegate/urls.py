from delegate.forms import DelegateProfileForm
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^username_autocomplete/$', 
        'autocomplete_app.views.username_autocomplete_all', 
        name='profile_username_autocomplete'),
    url(r'^$', 
        'basic_profiles.views.profiles', 
        name='profile_list'),
    url(r'^profile/(?P<username>[\w\._-]+)/$', 
        'basic_profiles.views.profile', 
        {'template_name': 'basic_profiles/delegate_profile.html'}, 
        name='profile_detail'),
    url(r'^edit/$', 
        'basic_profiles.views.profile_edit', 
        {'form_class': DelegateProfileForm}, 
        name='profile_edit'),
    url(r'^feed/$', 
        'delegate.views.feed_all', 
        name='delegate_feed_all'),
)
