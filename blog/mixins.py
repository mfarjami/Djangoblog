from django.shortcuts import redirect, get_object_or_404
from .models import Post

class AuthorAccessMixin():
    """
    Mixin to post only if the user is the author of the post
    """
    def dispatch(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_id)
        if request.user.is_authenticated:
            if request.user.is_admin or request.user.username == post.user.username:
                return super().dispatch(request, post_id, *args, **kwargs)
            else:
                return redirect('accounts:profile',  request.user.id )
        else:
            return redirect('accounts:login')