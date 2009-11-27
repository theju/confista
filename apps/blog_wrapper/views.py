from blog.views import new, edit, destroy
from django.contrib.syndication.views import feed
from blog_wrapper.feeds import AllBlogFeed, BlogUserFeed
from django.contrib.auth.decorators import permission_required

@permission_required("blog.add_post", login_url="/blog/not_authorized/")
def new_post(request):
    return new(request)

@permission_required("blog.change_post", login_url="/blog/not_authorized/")
def edit_post(request, **kwargs):
    return edit(request, **kwargs)

@permission_required("blog.delete_post", login_url="/blog/not_authorized/")
def destroy_post(request, **kwargs):
    return destroy(request, **kwargs)

def feed_all(request):
    url = 'feed/'
    return feed(request, url, {
        "feed": AllBlogFeed,
    })

def feed_user(request, username):
    url = 'feed/%s' %username
    return feed(request, url, {
        "feed": BlogUserFeed,
    })
