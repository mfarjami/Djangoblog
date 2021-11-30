from django.shortcuts import redirect, get_object_or_404


class AuthorAccessEditProfileMixin(object):
    """
    Mixin to add edit profile functionality to the author model.
    """
    def dispatch(self, request, username, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin or request.user.username == username:
                return super().dispatch(request, username, *args, **kwargs)
            else:
                return redirect('accounts:profile',  request.user.id )
        else:
            return redirect('accounts:login')
            