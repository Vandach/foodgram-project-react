from rest_framework import serializers
# from food.serializers import RecipeSecondSerializer
from users.models import User
from food.models import Recipe
# from food.serializers import RecipeSecondSerializer
from drf_extra_fields.fields import Base64ImageField


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
            'last_name',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Недопустимый username')
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'new_password', 'current_password',
        )




# class SubscriptionSerializer(UserSerializer):
#     recipes = RecipeSecondSerializer(many=True)
#     recipes_count = serializers.SerializerMethodField()

#     class Meta(UserSerializer.Meta):
#         fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count',)

#     def get_recipes_count(self, obj):
#         return obj.recipes.count()

