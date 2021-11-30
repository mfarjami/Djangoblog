from django.shortcuts import redirect

class AuthorsAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().dispatch(request, *args, **kwargs)
                
            else:
                return redirect('accounts:profile',  request.user.id )
        else:
            return redirect('accounts:login')