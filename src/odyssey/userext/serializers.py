from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'avatar', 'firstname', 'lastname',)
        read_only_fields = ('email', 'avatar',)


class NewUserSerializer(serializers.ModelSerializer):
    """
    Serializer for new user
    """
    class Meta:
        model = User
        fields = ('email', 'password')


class RestoreUserSerializer(serializers.Serializer):
    """
    Serializer for restoring user
    """
    email = serializers.EmailField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserInfoSerializer(serializers.Serializer):
    """
    Serializer for user info
    """
    firstname = serializers.CharField()
    lastname = serializers.CharField()


class AvatarSerializer(serializers.Serializer):
    """
    Serializer for image
    """
    avatar = serializers.ImageField()
