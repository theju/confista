from atomformat import Feed
from blog.models import Post
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

ITEMS_FEED=5

class AllBlogFeed(Feed):
    def feed_id(self):
        return "http://%s%s" %(Site.objects.get_current().domain,
                               reverse('blog_feed_all'))

    def feed_title(self):
        return "Feed of all blogs on %s" %(Site.objects.get_current().domain)

    def items(self):
        return Post.objects.order_by('updated_at')[:ITEMS_FEED]

    def item_id(self, item):
        return item.get_absolute_url()        

    def item_title(self, item):
        return item.title

    def item_updated(self, item):
        return item.updated_at

    def item_authors(self, item):
        return [{"name": item.author.username}]

    def item_links(self, item):
        return [{"href": item.get_absolute_url()}]

class BlogUserFeed(Feed):
    def get_object(self, param):
        self.username = param[0]

    def feed_id(self):
        return "http://%s%s" %(Site.objects.get_current().domain,
                               reverse('blog_feed_user', kwargs={'username':self.username}))

    def feed_title(self):
        return "Blog Feed of %s on %s" %(self.username,
                                         Site.objects.get_current().domain)

    def items(self):
        return Post.objects.filter(author__username=self.username).order_by('updated_at')[:ITEMS_FEED]

    def item_id(self, item):
        return item.get_absolute_url()        

    def item_title(self, item):
        return item.title

    def item_updated(self, item):
        return item.updated_at

    def item_authors(self, item):
        return [{"name": item.author.username}]

    def item_links(self, item):
        return [{"href": item.get_absolute_url()}]

