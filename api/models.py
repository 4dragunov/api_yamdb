from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

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


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=40)

    class Meta:
        ordering = ["-pub_date"]


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название жанра")
    slug = models.SlugField(max_length=40)

    class Meta:
        ordering = ["-pub_date"]


class Title(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название произведения")
    slug = models.SlugField(max_length=40)

    category = models.ForeignKey(
        Category,
        on_delete = models.SET_NULL,
        related_name="titles",
        verbose_name = "Категория"
    )
    
    genres = models.ManyToManyField(Genre)

    YEAR_CHOICES = [(r,r) for r in range(1984, datetime.date.today().year+1)]
    year = models.IntegerField(_('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    
    description = models.TextField(max_length=1000, verbose_name="Краткое описание произведения")
    
    score = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])

    class Meta:
        ordering = ["-pub_date"]