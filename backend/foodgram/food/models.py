from django.contrib.auth import get_user_model
from django.db import models
from datetime import timedelta
# from django.urls import reverse

from .constants import POST_STRING_LENGTH

User = get_user_model()


class Tag(models.Model):
    """Класс тагов"""

    title = models.CharField(
        max_length=200,
        verbose_name="Название тега",
    )

    def __str__(self):
        return self.title


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
    products = models.ForeignKey(
        'Product',
        related_name="recipe",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Продукты",
        )
    tags = models.ManyToManyField(Tag)
    time = models.DurationField(default=timedelta)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:POST_STRING_LENGTH]


class Product(models.Model):
    """Класс продукты"""

    title = models.CharField(
        max_length=200,
        verbose_name="Название группы",
    )

    def __str__(self):
        return self.title


# class Recipe(models.Model):
#     title = models.CharField(max_length=250, verbose_name='Название')
#     slug = models.SlugField(
#         max_length=150, db_index=True, verbose_name='URL'
#         )
#     content = models.TextField(blank=True)
#     photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
#     time_create = models.DateTimeField(
#         auto_now_add=True, verbose_name='Дата публикации'
#         )
#     time_update = models.DateTimeField(auto_now=True)
#     is_published = models.BooleanField(default=True)
#     cat = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)

#     def __str__(self) -> str:
#         return self.title

#     def get_absolute_url(self):
#         return reverse('recipe', kwargs={"recipe_slug": self.slug})

#     class Meta:
#         verbose_name = 'Рецепт'
#         verbose_name_plural = 'Рецепты'
#         ordering = ['time_create', 'title']


# class Category(models.Model):
#     name = models.CharField(
#         max_length=250, db_index=True, verbose_name='Категория'
#         )
#     slug = models.SlugField(
#         max_length=150, unique=True, db_index=True, verbose_name='URL'
#         )

#     def __str__(self) -> str:
#         return self.name

#     def get_absolute_url(self):
#         return reverse('category', kwargs={"cat_slug": self.slug})

#     class Meta:
#         verbose_name = 'Категория'
#         verbose_name_plural = 'Категории'
#         ordering = ['id']


# class Recipe2(models.Model):
#     title = models.CharField(max_length=250, verbose_name='Название')
#     slug = models.SlugField(
#         max_length=150, db_index=True, verbose_name='URL'
#         )
#     photo = models.ImageField(
# null=True, blank=True, upload_to="photos/%Y/%m/%d/",
# verbose_name='Изображения')
