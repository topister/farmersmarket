from django.core.exceptions import PermissionDenied

def user_is_buyer(function):

    def wrap(request, *args, **kwargs):   

        if request.user.role == 'buyer':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap



def user_is_farmer(function):

    def wrap(request, *args, **kwargs):    

        if request.user.role == 'farmer':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap