from datetime import timedelta

from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models
# from ..users.models import User
from users.models import User

from .constants import POST_STRING_LENGTH


# User = get_user_model()


class Tag(models.Model):
    """Класс тагов"""

    title = models.CharField(
        max_length=200,
        verbose_name="Название тега",
    )
    color = ColorField(default='#FF0000', blank=True)
    slug = models.SlugField(max_length=150, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title


class Product(models.Model):
    """Класс продукты"""

    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Ед. измирения",
        blank=True,
    )

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class Recipe(models.Model):
    """Класс Рецепта"""
    author = models.ForeignKey(
        User,
        related_name="recipe",
        on_delete=models.CASCADE,
        verbose_name="Автор",
        )
    title = models.CharField(
        max_length=250, verbose_name='Название'
        )
    text = models.TextField(verbose_name="Текст")
    photo = models.ImageField(
        null=True, blank=True, upload_to="photos/%Y/%m/%d/",
        verbose_name='Изображения'
        )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
        )
    products = models.ManyToManyField(Product, through="Enrollment")
    tags = models.ManyToManyField(Tag)
    time = models.DurationField(default=timedelta)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.title[:POST_STRING_LENGTH]


class Enrollment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    ammount = models.CharField(
        max_length=250, verbose_name='Количество'
        )

    def __str__(self):
        return "{}_{}".format(self.recipe.__str__(), self.products.__str__())
