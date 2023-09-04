DJOSER = {
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'activation': ['rest_framework.permissions.AllowAny'],
        'password_reset': ['rest_framework.permissions.IsAuthenticated'],
        'password_reset_confirm': ['rest_framework.permissions.IsAuthenticated'],
        'set_password': ['rest_framework.permissions.IsAuthenticated'],
        'username_reset': ['rest_framework.permissions.IsAuthenticated'],
        'username_reset_confirm': ['rest_framework.permissions.IsAuthenticated'],
        'set_username': ['rest_framework.permissions.IsAuthenticated'],
        'user_create': ['apps.common_services.permissions.IsAdmin'],
        'user_delete': ['apps.common_services.permissions.IsAdmin'],
        'user': ['djoser.permissions.CurrentUserOrAdminOrReadOnly'],
        'user_list': ['apps.common_services.permissions.IsAdmin'],
        'token_create': ['rest_framework.permissions.IsAuthenticated'],
        'token_destroy': ['rest_framework.permissions.IsAuthenticated'],
    },
    'SERIALIZERS': {
        'current_user': 'apps.users.api.v1.serializers.UserSerializer',
        'user': 'apps.users.api.v1.serializers.UserSerializer',
        # 'user_create': 'apps.users.api.v1.serializers.UserCreateSerializer',
    },
}
