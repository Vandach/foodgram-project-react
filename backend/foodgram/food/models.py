from colorfield.fields import ColorField
from django.db import models
# from ..users.models import User
from users.models import User

from .constants import POST_STRING_LENGTH


# User = get_user_model()


class Tag(models.Model):
    """Класс тагов"""

    name = models.CharField(
        max_length=200,
        verbose_name="Название тега",
    )
    color = ColorField(default='#FF0000', blank=True)
    slug = models.SlugField(max_length=150, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
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
    # amount = models.IntegerField()

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
    name = models.CharField(
        max_length=250, verbose_name='Название'
        )
    text = models.TextField(verbose_name="Текст")
    image = models.ImageField(
        null=True, blank=True, upload_to="photos/%Y/%m/%d/",
        verbose_name='Изображения'
        )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
        )
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredients"
        )
    tags = models.ManyToManyField(Tag)
    cooking_time = models.IntegerField()
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.name[:POST_STRING_LENGTH]


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class ShoppingCart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='User'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Recipe'
    )

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в корзину покупок'