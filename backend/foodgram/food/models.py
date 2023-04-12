from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
from datetime import timedelta
# from django.urls import reverse

from .constants import POST_STRING_LENGTH

User = get_user_model()

# class User(AbstractUser):
#     USER = 'user'
#     MODERATOR = 'moderator'
#     ADMIN = 'admin'
#     USER_ROLES = (
#         (USER, 'User'),
#         (MODERATOR, 'Moderator'),
#         (ADMIN, 'Admin'),
#     )
#     email = models.EmailField(
#         'Email', max_length=254, unique=True, null=False, blank=False
#     )
#     is_subscribed = models.BooleanField(default=False)
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name='user permissons',
#         blank=True,
#         related_name='user_permissions_user',
#     )
#     groups = models.ManyToManyField(
#         Group,
#         verbose_name='groups',
#         blank=True,
#         related_name='user_group_set',
#         related_query_name='user'
#     )
#     @property
#     def is_admin(self):
#         return (
#             self.role == self.ADMIN
#             or self.is_superuser
#             or self.is_staff
#         )
#     @property
#     def is_moderator(self):
#         return self.role == self.MODERATOR

#     def __str__(self):
#         return self.username


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
    

# class Product(models.Model):
#     """Класс продукты"""

#     name = models.CharField(
#         max_length=200,
#         verbose_name="Название группы",
#     )

#     measurement_unit = models.CharField(
#         max_length=200,
#         verbose_name="Мера",
#     )

#     def __str__(self):
#         return self.title


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
