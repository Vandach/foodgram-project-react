from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс Пользователя"""

    email = models.EmailField(
        'Email', max_length=254, unique=True, null=False, blank=False
    )
    is_subscribed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Класс подписки"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name_plural = 'Подписки'
        verbose_name = 'Подписка'
