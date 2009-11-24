from blog.views import new, edit, destroy
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
