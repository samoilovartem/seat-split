from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, password, first_name, last_name, **extra_fields):
        if not username:
            raise ValueError('Username must be provided')
        if not first_name:
            raise ValueError('User must have a first name')
        if not last_name:
            raise ValueError('User must have a last name')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(
        self, username, password, first_name, last_name=None, **extra_fields
    ):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            username, password, first_name, last_name, **extra_fields
        )

    def create_superuser(
        self, username, password, first_name, last_name, **extra_fields
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            username, password, first_name, last_name, **extra_fields
        )


class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, blank=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, blank=True)
    team = models.CharField(max_length=50, blank=True)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ('first_name', 'last_name')
