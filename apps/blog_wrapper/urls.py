from blog.forms import BlogForm
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    # blog post
    url(r'^post/(?P<username>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$', 'blog.views.post', name='blog_post'),

    # all blog posts
    url(r'^$', 'blog.views.blogs', name="blog_list_all"),

    # blog post for user
    url(r'^posts/(?P<username>\w+)/$', 'blog.views.blogs', name='blog_list_user'),

    # your posts
    url(r'^your_posts/$', 'blog.views.your_posts', name='blog_list_yours'),

    # new blog post
    url(r'^new/$', 'blog_wrapper.views.new_post', name='blog_new'),

    # edit blog post
    url(r'^edit/(\d+)/$', 'blog_wrapper.views.edit_post', name='blog_edit'),

    #destory blog post
    url(r'^destroy/(\d+)/$', 'blog_wrapper.views.destroy_post', name='blog_destroy'),

    # ajax validation
    (r'^validate/$', 'ajax_validation.views.validate', {'form_class': BlogForm, 'callback': lambda request, *args, **kwargs: {'user': request.user}}, 'blog_form_validate'),

    # 403 Error to users who can't add posts
    (r'^not_authorized/$', direct_to_template, {'template': 'blog/blog_403.html'}),

    # Feeds URL. For specific user
    url(r'^feed/(?P<username>[-\w]+)/$', 'blog_wrapper.views.feed_user', name='blog_feed_user'),

    # Feeds URL. For all the blogs
    url(r'^feed/$', 'blog_wrapper.views.feed_all', name='blog_feed_all'),

)
