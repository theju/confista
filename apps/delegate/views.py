from delegate.feeds import DelegateFeed
from django.contrib.syndication.views import feed

def feed_all(request):
    url = "feed/"
    return feed(request, url, {
            "feed": DelegateFeed,
            })
