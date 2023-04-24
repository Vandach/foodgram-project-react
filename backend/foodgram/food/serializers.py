from rest_framework import serializers, exceptions
from users.serializers import UserSerializer
from drf_writable_nested import WritableNestedModelSerializer
from .models import Recipe, RecipeIngredients, Tag, Ingredient
from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404

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

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    ingredients = RecipeIngredientsSerializer(
        many=True, source="recipeingredients_set"
        )
    tags = serializers.SerializerMethodField()
    # tags = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Tag.objects.all()
    #     )

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
    # amount = serializers.IntegerField(validators=(
    #     MinValueValidator(1, message='Количество должно быть больше нуля.'),))
    amount = serializers.IntegerField()
    
    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class CreateRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(source='get_id')
    name = serializers.SerializerMethodField(source='get_name')
    measurement_unit = serializers.SerializerMethodField(
        source='get_measurement_unit'
        )

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurment_unit(self, obj):
        return obj.ingredient.measurement_unit

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')





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




class RecipeCreateSerializer(WritableNestedModelSerializer,
                             serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = Ingredient2RecipeSerializer(
        many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
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

    def validate_ingredients(self, value):
        if not value:
            raise exceptions.ValidationError(
                'Нужно добавить ингридиенты.'
                )
        ingredients_check = [item['id'] for item in value]
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
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(author=author, **validated_data)
        # recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        for ing in ingredients:
            amount = ing['amount']
            ingredientdone = get_object_or_404(Ingredient, name=ing['id'])
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=ingredientdone,
                amount=amount,
            )

        return recipe



    # def create_ingredients(self, recipe, ingredients):
    #     RecipeIngredients.objects.bulk_create([
    #         RecipeIngredients(
    #             recipe=recipe,
    #             amount=ingredient['amount'],
    #             ingredient=ingredient['ingredient'],
    #         ) for ingredient in ingredients
    #     ])

    # def create(self, validated_data):
    #     ingredients = validated_data.pop('ingredients')
    #     recipe = Recipe.objects.create(**validated_data)
    #     self.create_ingredients(recipe, ingredients)
    #     return recipe
