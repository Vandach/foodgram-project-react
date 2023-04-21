from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import Recipe, Enrollment, Tag, Ingredients


class EnrollmentSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit'
        )

    class Meta:
        model = Enrollment
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    ingredients = EnrollmentSerializer(many=True, source="enrollment_set")
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


class EnrollmentCreateSerializer(WritableNestedModelSerializer,
                                 serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='ingredients.id'
        )

    class Meta:
        model = Enrollment
        fields = ('id', 'amount')


class CreateRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all(),
        source='ingredient')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit', 'amount')



class RecipeCreateSerializer(WritableNestedModelSerializer,
                             serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    ingredients = EnrollmentCreateSerializer(
        many=True)
    tags = serializers.SerializerMethodField()

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

    def create_ingredients(self, recipe, ingredients):
        Enrollment.objects.bulk_create([
            Enrollment(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredient=ingredient['id'],
            ) for ingredient in ingredients
        ])

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(recipe, ingredients)
        return recipe

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color',
            'slug',
        )
