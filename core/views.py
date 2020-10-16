from django.db import IntegrityError
from rest_framework import permissions, generics, views
from rest_framework.parsers import FileUploadParser
from rest_framework.mixins import UpdateModelMixin
from PIL import Image
from django.core.files.storage import default_storage
from . import permissions as custom_permissions
from rest_framework.response import Response
from . import serializers
from .models import User, UserSkill


class UserCreate(generics.CreateAPIView):
    serializer_class = serializers.UserCreateSerializer
    permission_classes = (permissions.AllowAny,)


class UserUpdate(generics.GenericAPIView, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.UserUpdateSerializer
    permission_classes = (custom_permissions.TokenMatches,)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserUpdateAvatar(views.APIView):
    parser_classes = [FileUploadParser]
    permission_classes = (custom_permissions.TokenMatches,)
    queryset = User.objects.all()

    def put(self, request, id, format=None):
        try:
            user = self.queryset.get(id=id)
            self.check_object_permissions(self.request, user)

            file_obj = request.data['file']
            Image.open(file_obj)

            if user.avatar.name:
                default_storage.delete(user.avatar.path)

            user.avatar = file_obj
            user.save()
            response_data = serializers.UserUpdateSerializer(user).data
            return Response(data=response_data, status=200)

        except IOError:
            return Response(data={'detail': 'Invalid file type.'}, status=400)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserListSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'id'


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserListSerializer
    permission_classes = (permissions.AllowAny,)


class SkillCreate(views.APIView):
    serializer_class = serializers.SkillCreateSerializer
    permission_classes = (custom_permissions.TokenMatches,)

    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
            self.check_object_permissions(self.request, user)
            user_skill = UserSkill(user=user, skill=request.data['skill'])
            user_skill.save()
            response_data = self.serializer_class(user_skill).data
            return Response(data=response_data, status=200)
        except KeyError:
            return Response(data={'detail': 'Missing field.', 'missing': 'skill'}, status=400)
        except IntegrityError:
            return Response(data={'detail': 'This record has been created before.'}, status=400)


class SkillDelete(views.APIView):
    queryset = UserSkill.objects.all()
    serializer_class = serializers.SkillCreateSerializer
    permission_classes = (custom_permissions.TokenMatches,)

    def delete(self, request, user_id, skill_id):
        user = User.objects.get(id=user_id)
        user_skill = self.queryset.get(id=skill_id, user_id=user_id)
        self.check_object_permissions(self.request, user)
        user_skill.delete()
        return Response(data={'detail': 'Object deleted.'}, status=200)