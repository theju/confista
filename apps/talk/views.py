from talk.models import Talk
from talk.forms import TalkForm
from talk.feeds import TalkFeed
from django.template import RequestContext
from deadline.utils import deadline_expired
from django.shortcuts import render_to_response
from django.contrib.syndication.views import feed
from django.contrib.auth.decorators import login_required

def render(request, template, context_dict=None):
    return render_to_response(
        template, context_dict or {}, context_instance=RequestContext(request)
    )

def list(request, id=None):
    if id:
        talks = [Talk.objects.get(id=id),]
        template_file = 'talk/talk_id.html'
    else:
        talks = Talk.objects.all()
        template_file = 'talk/talk_list.html'
    return render(request, template_file, {'talks': talks})

@deadline_expired("talk_submission")
@login_required
def add_talk(request):
    if request.method == "POST":
        talk_form = TalkForm(request.POST, user=request.user)
        if talk_form.is_valid():
            talk_form.save()
            request.user.message_set.create(
                message="Talk %(title)s successfully added." % {"title": talk_form.cleaned_data['title']})
    else:
        talk_form = TalkForm(user=request.user)
    return render(request, 'talk/talk_form.html', {'form': talk_form})

def feed_all(request):
    url = "feed/"
    return feed(request, url, {
            "feed": TalkFeed,
            })
