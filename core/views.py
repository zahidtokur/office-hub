from rest_framework import permissions, generics, views, status
from rest_framework.parsers import FileUploadParser
from rest_framework.mixins import UpdateModelMixin
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
    permission_classes = (custom_permissions.IsOwner,)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserUpdateAvatar(views.APIView):
    parser_classes = [FileUploadParser]
    permission_classes = (custom_permissions.IsOwner,)
    queryset = User.objects.all()

    def put(self, request, id, format=None):
        user = self.queryset.get(id=id)
        self.check_object_permissions(self.request, user)
        file_obj = request.data['file']
        user.avatar = file_obj
        user.save()
        return Response(status=200)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserListSerializer
    permission_classes = (permissions.AllowAny,)


class SkillCreate(views.APIView):
    serializer_class = serializers.SkillCreateSerializer
    permission_classes = (custom_permissions.IsOwner,)

    def post(self, request, id):
        user = User.objects.get(id=id)
        self.check_object_permissions(self.request, user)
        user_skill = UserSkill(user=user, skill=request.data['skill'])
        user_skill.save()
        response_data = self.serializer_class(user_skill).data
        return Response(data=response_data, status=status.HTTP_200_OK)


class SkillDelete(views.APIView):
    queryset = UserSkill.objects.all()
    serializer_class = serializers.SkillCreateSerializer
    permission_classes = (custom_permissions.IsOwner,)

    def delete(self, request, user_id, skill_id):
        user = User.objects.get(id=user_id)
        user_skill = self.queryset.get(id=skill_id, user_id=user_id)
        self.check_object_permissions(self.request, user)
        user_skill.delete()
        return Response(data={'detail': 'Object deleted.'}, status=status.HTTP_200_OK)