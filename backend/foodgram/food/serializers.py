from rest_framework import serializers
from .models import Recipe, Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit'
        )

    class Meta:
        model = Enrollment
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    ingredients = EnrollmentSerializer(many=True, source="enrollment_set")

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time',)

    def get_tags(self, obj):
        return [{
            "id": tag.id,
            "name": tag.title,
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
