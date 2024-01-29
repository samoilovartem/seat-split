from rest_framework.permissions import SAFE_METHODS, BasePermission, DjangoModelPermissions


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


class CurrentUserOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        if request.user.is_staff or request.user.is_superuser:
            return True


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser


class IsTicketHolder(BasePermission):
    message = 'User is not a ticket holder.'

    def has_permission(self, request, view):
        # Allow ticket access if user is a ticket holder or if they're a staff member or superuser
        return (
            hasattr(request.user, 'ticket_holder_user') or request.user.is_staff or request.user.is_superuser
        )
