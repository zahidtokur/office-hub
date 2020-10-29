from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User, UserSkill


class RegisterSerializer(serializers.ModelSerializer):
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



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'job_title', 'self_description', 'avatar', 'registered_date', 'skills')
        depth = 1
        extra_kwargs = {
            'username' : {'read_only': True},
        }


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = ('id', 'user', 'skill')