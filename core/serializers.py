from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'token', 'username', 'password', 'first_name', 'last_name', 'job_title', 'self_description', 'avatar', 'registered_date')
        extra_kwargs = {
            'avatar': {'read_only': True},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_auth_token(self, obj):
        token = Token.objects.get(user=obj)
        return token.key



class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'job_title', 'self_description',)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'job_title', 'self_description', 'avatar', 'registered_date')
        extra_kwargs = {
            'username' : {'read_only': True},
            'avatar': {'read_only': True},
        }
