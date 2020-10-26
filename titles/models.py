from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=40, unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название жанра",
                            blank=False)
    slug = models.SlugField(max_length=40, unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название произведения")
    # YEAR_CHOICES = [(r, r) for r in range(1984, datetime.date.today().year + 1)]
    # year = models.IntegerField('year', choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    year = models.PositiveIntegerField(default=datetime.datetime.now().year)
    rating = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)], null=True, )
    description = models.TextField(max_length=1000, verbose_name="Краткое описание произведения")
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name="Категория"
    )
    slug = models.SlugField(max_length=40)
