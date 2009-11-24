from django.shortcuts import render_to_response
from django.template import RequestContext
from talk.models import Talk, Topic, Level
from delegate.models import Delegate_Profile, Occupation, Location

def get_name_count(qs, model, field_attr):
    lst = []
    for item in qs:
        num_by_item = model.objects.filter(**{field_attr :item.name}).count()
        lst.append((item.name, num_by_item))
    return lst

def list_all(request):
    num_talks = Talk.objects.count()
    num_delegates = Delegate_Profile.objects.count()
    num_talks_by_topic = get_name_count(Topic.objects.all(), Talk, 'topic__name')
    num_talks_by_level = get_name_count(Level.objects.all(), Talk, 'level__name')
    num_delegates_by_occupation = get_name_count(Occupation.objects.all(), Delegate_Profile, 'occupation__name')
    num_delegates_by_location   = get_name_count(Location.objects.all(), Delegate_Profile, 'location__name')
    return render_to_response('statistics/statistics_list.html',
                              {'num_talks': num_talks,
                               'num_delegates': num_delegates,
                               'num_talks_by_topic': num_talks_by_topic,
                               'num_talks_by_level': num_talks_by_level,
                               'num_delegates_by_occupation': num_delegates_by_occupation,
                               'num_delegates_by_location': num_delegates_by_location},
                              context_instance = RequestContext(request))
