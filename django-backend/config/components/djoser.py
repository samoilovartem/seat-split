DJOSER = {
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'activation': ['rest_framework.permissions.IsAuthenticated'],
        'password_reset': ['rest_framework.permissions.IsAuthenticated'],
        'password_reset_confirm': ['rest_framework.permissions.IsAuthenticated'],
        'set_password': ['rest_framework.permissions.IsAuthenticated'],
        'username_reset': ['rest_framework.permissions.IsAuthenticated'],
        'username_reset_confirm': ['rest_framework.permissions.IsAuthenticated'],
        'set_username': ['rest_framework.permissions.IsAuthenticated'],
        'user_create': [
            'apps.common_services.permissions.CustomDjangoModelPermissions'
        ],
        'user_delete': [
            'apps.common_services.permissions.CustomDjangoModelPermissions'
        ],
        'user': ['rest_framework.permissions.IsAuthenticated'],
        'user_list': ['apps.common_services.permissions.CustomDjangoModelPermissions'],
        'token_create': ['rest_framework.permissions.IsAuthenticated'],
        'token_destroy': ['rest_framework.permissions.IsAuthenticated'],
    },
    'SERIALIZERS': {
        'current_user': 'apps.users.api.v1.serializers.UserDetailSerializer',
        'user': 'djoser.serializers.UserSerializer',
        'user_create': 'djoser.serializers.UserCreateSerializer',
    },
}
