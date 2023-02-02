from functools import wraps
from rest_framework import status
from rest_framework.response import Response


def user_role_check(role_check=()):
    """ This decorator takes arguments and return response of decorated function"""

    def view_wrapper_function(decorated_view_function):
        """ This intermediate wrapper function takes the decorated View function (e.g. get, post) itself. """
    
        @wraps(decorated_view_function)
        def check_user_permissions(view, request, *args, **kwargs):
            """ A function that checks user permissions """
            permissions_evaluations = map(lambda role: getattr(request.user, role, False), role_check)
            is_authorized = any(permissions_evaluations)

            if not is_authorized:
                return Response("You are authenticated but unauthorized!", status=status.HTTP_403_FORBIDDEN)

            response =  decorated_view_function(view, request, *args, **kwargs)
            
            return response
    
        return check_user_permissions
    
    return view_wrapper_function


from rest_framework.permissions import BasePermission

class IsSupportMember(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_support:
            return False
        return True