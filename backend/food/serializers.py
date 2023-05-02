from django.shortcuts import get_object_or_404
from rest_framework import serializers, exceptions
from users.serializers import UserSerializer
from drf_writable_nested import WritableNestedModelSerializer
from .models import Recipe, RecipeIngredients, Tag, Ingredient
from django.core.validators import MinValueValidator
from .utils import recipe_ingredient_create
from collections import OrderedDict
from drf_extra_fields.fields import Base64ImageField


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
    id = serializers.SerializerMethodField(method_name='get_id')
    name = serializers.SerializerMethodField(method_name='get_name')
    measurement_unit = serializers.SerializerMethodField(
        method_name='get_measurement_unit'
    )
    amount = serializers.SerializerMethodField(method_name='get_amount')

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    def get_amount(self, obj):
        return obj.amount

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    ingredients = RecipeIngredientsSerializer(
        many=True, source="recipeingredients_set"
        )
    tags = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time',)

    def get_tags(self, obj):
        return [{
            "id": tag.id,
            "name": tag.name,
            "color": tag.color,
            "slug": tag.slug
            } for tag in obj.tags.all()]

    def get_author(self, obj):
        return {
            "email": obj.author.email,
            "id": obj.author.id,
            "username": obj.author.username,
            "first_name": obj.author.first_name,
            "last_name": obj.author.last_name,
            "is_subscribed": obj.author.is_subscribed,
            }

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


class RecipeIngredientsCreateSerializer(WritableNestedModelSerializer,
                                        serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='ingredient.id'
        )

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class CreateIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        fields = ('id', 'amount',)


class CreateRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class Ingredient2RecipeSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    amount = serializers.IntegerField(write_only=True, min_value=1)
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount', 'recipe')


class RecipeIngredients2Serializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount',)

    def to_representation(self, instance):
        old_repr = super().to_representation(instance)
        new_repr = OrderedDict()
        new_repr['id'] = old_repr['id']
        new_repr['name'] = instance.ingredient.name
        new_repr['measurement_unit'] = instance.ingredient.measurement_unit
        new_repr['amount'] = old_repr['amount']
        return new_repr


class RecipeCreateSerializer(WritableNestedModelSerializer,
                             serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredients2Serializer(
        source='recipeingredients_set',
        many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
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

    def get_author(self, obj):
        return {
            "email": obj.author.email,
            "id": obj.author.id,
            "username": obj.author.username,
            "first_name": obj.author.first_name,
            "last_name": obj.author.last_name,
            "is_subscribed": obj.author.is_subscribed,
            }

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

    def validate_ingredients(self, value):
        if not value:
            raise exceptions.ValidationError(
                'Нужно добавить ингридиенты.'
                )
        check = self.initial_data.get('ingredients')
        ingredients_check = [item['id'] for item in check]
        for ingredient in ingredients_check:
            if ingredients_check.count(ingredient) > 1:
                raise exceptions.ValidationError(
                    'У рецепта не может быть два одинаковы ингридиента'
                )
        return value

    def validate_tags(self, value):
        if not value:
            raise exceptions.ValidationError(
                'Нужно добавить тег.'
                )
        return value

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('recipeingredients_set')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        recipe_ingredient_create(ingredients, RecipeIngredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredients_set')
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        recipe_ingredient_create(ingredients, RecipeIngredients, instance)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        tag_id_list, tag_list = repr['tags'], []
        for tag_id in tag_id_list:
            tag = get_object_or_404(Tag, id=tag_id)
            serialized_tag = OrderedDict(TagSerializer(tag).data)
            tag_list.append(serialized_tag)
        repr['tags'] = tag_list
        return repr


class RecipeSecondSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
