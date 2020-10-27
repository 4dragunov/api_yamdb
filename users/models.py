from django.core.validators import validate_email
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    """Расширение стандартной модели пользователя Django"""
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=False, unique=True,
                              validators=[validate_email, ])
    role = models.CharField(
        max_length=9, blank=False, choices=UserRole.choices,
        default=UserRole.USER
    )
    secret = models.CharField(max_length=20)
    username = models.CharField(max_length=20,
                                blank=True,
                                null=True,
                                unique=True,
                                db_index=True)
