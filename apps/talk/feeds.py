from atomformat import Feed
from talk.models import Talk
from datetime import datetime
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

ITEMS_FEED=5

class TalkFeed(Feed):
    def feed_id(self):
        return "http://%s%s" %(Site.objects.get_current().domain,
                               reverse('talk_feed_all'))

    def feed_title(self):
        return "Feed of talks added on %s" %(Site.objects.get_current().domain)

    def items(self):
        return Talk.objects.all()[:ITEMS_FEED]

    def item_id(self, item):
        return reverse("talk_list_id", kwargs={"id": item.id})

    def item_title(self, item):
        return item.title

    def item_updated(self, item):
        # Very hackish, because the Talk model does
        # not have any field to store the creation time
        # Probably a TODO
        return datetime.now()

    def item_authors(self, item):
        for speaker in item.speakers.all():
            yield {"name": speaker.username}

    def item_links(self, item):
        return [{"href": reverse("talk_list_id", kwargs={"id": item.id})}]
