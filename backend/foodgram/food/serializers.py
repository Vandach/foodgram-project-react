from rest_framework import serializers
from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()


    class Meta:
        model = Recipe
        fields = '__all__'

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