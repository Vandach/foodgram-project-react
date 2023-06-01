from colorfield.fields import ColorField
from django.db import models
from django.core.validators import (RegexValidator, MinValueValidator)

from users.models import User
from .constants import POST_STRING_LENGTH


class Tag(models.Model):
    """Класс тагов"""

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тега',
    )
    color = ColorField(
        default='#00ff00',
        format='hex',
        max_length=7,
        unique=True,
        verbose_name='Цвет тега',
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Введите формат HEX. Пример: #00ff00',
            )
        ],
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        db_index=True,
        verbose_name='URL')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Класс продукты"""

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Ед. измирения',
        blank=True,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'),
        )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Класс Рецепта"""
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=250,
        verbose_name='Название'
    )
    text = models.TextField(verbose_name='Текст')
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='food/images/',
        verbose_name='Изображения',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        verbose_name='Ингредиенты рецепта',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
    )
    cooking_time = models.SmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(
            1, message='Рецепт не может готовиться меньше минуты.'
        )
        ]
    )
    is_favorited = models.BooleanField(verbose_name='Избранный')
    is_in_shopping_cart = models.BooleanField(verbose_name='Список покупок')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(fields=['author', 'name'],
                                    name='unique_author_name')
        ]

    def __str__(self) -> str:
        return self.name[:POST_STRING_LENGTH]


class RecipeIngredients(models.Model):
    """Класс ингредиентов в рецепте"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amount',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='amount',
        verbose_name='Ингредиент',
    )
    amount = models.IntegerField(verbose_name='Количество')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'],
                                    name='unique_recipe_ingredient')
        ]

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class ShoppingCart(models.Model):
    """Класс списка покупок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_cart_recipe')
        ]

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в корзину покупок'


class Favorite(models.Model):
    """Класс избранного"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite_recipe')
        ]

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в избранное'
