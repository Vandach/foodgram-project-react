from collections import OrderedDict

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import exceptions, serializers

from users.models import Follow, User
from food.models import (Ingredient, Recipe,
                         RecipeIngredients, Tag,
                         ShoppingCart, Favorite)

from .fields import Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Недопустимый username')
        return value

    def get_is_subscribed(self, value):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=value).exists()


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password'
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Недопустимый username')
        return value

    def validate_password(self, value):
        return make_password(value)


class ChangePasswordSerializer(serializers.Serializer):

    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'new_password', 'current_password',
        )


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = ('author', 'user', )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('author', 'user', ),
                message='Вы уже подписаны'
            )
        ]

    def create(self, validated_data):
        return Follow.objects.create(
            user=self.context.get('request').user, **validated_data
        )

    def validate_author(self, value):
        if self.context.get('request').user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя!'
            )
        return value


class SubscriptionInfoSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get(
            'recipes_limit', settings.PAGE_SIZE)
        queryset = obj.author.recipes.all()[:int(recipes_limit)]
        return RecipeShortSerializer(
            queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color',
            'slug',
        )


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'amount', 'measurement_unit', )


class RecipeIngredientsAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientsSerializer(
        many=True, source='amount'
    )
    tags = TagSerializer(read_only=True, many=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time',)

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping.filter(recipe=obj).exists()

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorite.filter(recipe=obj).exists()


class RecipeCreateSerializer(WritableNestedModelSerializer,
                             serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientsAmountSerializer(
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)
    cooking_time = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1,
                message='Время приготовление должно быть не менее 1 минуты'
            ),
        )
    )

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time',)

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise exceptions.ValidationError(
                'Нужно добавить ингридиенты.'
            )
        check = self.initial_data.get('ingredients')
        ingredients_check = [item['id'] for item in check]
        for ingredient in ingredients_check:
            if ingredients_check.count(ingredient) > 1:
                raise exceptions.ValidationError(
                    'У рецепта не может быть два одинаковых ингридиента.'
                )
        for ingredient in ingredients:
            if int(ingredient.get('amount')) < 1:
                raise exceptions.ValidationError(
                    'Количество ингредиента должно быть больше 0.'
                )
        return ingredients

    def validate_tags(self, tags):
        if not tags:
            raise exceptions.ValidationError(
                'Нужно добавить тег.'
            )
        return tags

    def add_ingredients_and_tags(self, tags, ingredients, recipe):
        for tag in tags:
            recipe.tags.add(tag)
            recipe.save()
        RecipeIngredients.objects.bulk_create([RecipeIngredients(
            ingredient_id=ingredient.get('id'),
            amount=ingredient.get('amount'),
            recipe=recipe
        ) for ingredient in ingredients])
        return recipe

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        return self.add_ingredients_and_tags(
            tags, ingredients, recipe
        )

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        return self.add_ingredients_and_tags(
            tags, ingredients, instance
        )

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        tag_id_list, tag_list = repr['tags'], []
        for tag_id in tag_id_list:
            tag = get_object_or_404(Tag, id=tag_id)
            serialized_tag = OrderedDict(TagSerializer(tag).data)
            tag_list.append(serialized_tag)
        repr['tags'] = tag_list
        return repr


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('user', 'recipe',)
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe', ),
                message='Рецепт уже добавлен!'
            )
        ]

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe',)
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe', ),
                message='Рецепт уже добавлен!'
            )
        ]

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
