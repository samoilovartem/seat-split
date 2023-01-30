DJOSER = {
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'activation': ['apps.permissions.CustomDjangoModelPermissions'],
        'password_reset': ['apps.permissions.IsOwnerOrReadOnly'],
        'password_reset_confirm': ['apps.permissions.IsOwnerOrReadOnly'],
        'set_password': ['apps.permissions.IsOwnerOrReadOnly'],
        'username_reset': ['apps.permissions.IsOwnerOrReadOnly'],
        'username_reset_confirm': ['rest_framework.permissions.AllowAny'],
        'set_username': ['apps.permissions.IsOwnerOrReadOnly'],
        # 'user_create': ['config.permissions.CustomDjangoModelPermissions'],
        'user_create': [
            'rest_framework.permissions.AllowAny'
            if DEBUG
            else 'apps.permissions.CustomDjangoModelPermissions'
        ],
        'user_delete': ['apps.permissions.CustomDjangoModelPermissions'],
        'user': ['apps.permissions.IsOwnerOrReadOnly'],
        'user_list': ['apps.permissions.CustomDjangoModelPermissions'],
        'token_create': ['rest_framework.permissions.AllowAny'],
        'token_destroy': ['rest_framework.permissions.AllowAny'],
    },
}
