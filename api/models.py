from django.db import models
from django.contrib.auth.models import AbstractUser

class UserRole(models.TextChoices):
    USER = 'USER'
    MODERATOR = 'MODERATOR'
    ADMIN = 'ADMIN'

class User(AbstractUser):
    """Расширение стандартной модели пользователя Django"""
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=False, unique=True)
    role = models.CharField(
        max_length=9, blank=False, choices=UserRole.choices, default=UserRole.USER
    )

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []
