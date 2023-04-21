from rest_framework import serializers
from users.models import User


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
