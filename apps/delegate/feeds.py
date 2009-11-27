from atomformat import Feed
from delegate.models import Delegate_Profile
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

ITEMS_FEED=5

class DelegateFeed(Feed):
    def feed_id(self):
        return "http://%s%s" %(Site.objects.get_current().domain,
                               reverse('delegate_feed_all'))

    def feed_title(self):
        return "Feed of delegates registered on %s" %(Site.objects.get_current().domain)

    def items(self):
        return Delegate_Profile.objects.order_by('-user__date_joined')[:ITEMS_FEED]

    def item_id(self, item):
        return item.get_absolute_url()

    def item_title(self, item):
        return item.user.username

    def item_updated(self, item):
        return item.user.date_joined

    def item_authors(self, item):
        return [{"name": item.user.username}]

    def item_links(self, item):
        return [{"href": item.get_absolute_url()}]
