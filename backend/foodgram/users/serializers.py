from rest_framework import serializers
# from django.contrib.auth import get_user_model

# User = get_user_model()

from users.models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('email', 'id', 'username', 'first_name', 'last_name')


class UserSerializer(serializers.ModelSerializer):

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
