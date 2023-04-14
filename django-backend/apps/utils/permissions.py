from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    DjangoModelPermissions,
)


class CustomDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = {
            'GET': ['%(app_label)s.view_%(model_name)s'],
            'OPTIONS': [],
            'HEAD': [],
            'POST': ['%(app_label)s.add_%(model_name)s'],
            'PUT': ['%(app_label)s.change_%(model_name)s'],
            'PATCH': ['%(app_label)s.change_%(model_name)s'],
            'DELETE': ['%(app_label)s.delete_%(model_name)s'],
        }


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.username == request.user


class SpecificTeamObjectOnly(BasePermission):
    """Gives access to an object if current user suits the condition"""

    def has_object_permission(self, request, view, obj):
        # if request.user.email == 'lawns@lawns.com':
        #     return obj.team == 'lawns'
        return obj.team == 'lawns' if request.user.email == 'lawns@lawns.com' else None
