from rest_framework import permissions, generics, views, status
from rest_framework.parsers import FileUploadParser
from rest_framework.mixins import UpdateModelMixin
from . import permissions as custom_permissions
from rest_framework.response import Response
from . import serializers
from .models import User


class Create(generics.CreateAPIView):
    serializer_class = serializers.UserCreateSerializer
    permission_classes = (permissions.AllowAny,)


class Update(generics.GenericAPIView, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.UserUpdateSerializer
    permission_classes = (custom_permissions.IsOwner,)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UploadAvatar(views.APIView):
    parser_classes = [FileUploadParser]
    permission_classes = (custom_permissions.IsOwner,)
    queryset = User.objects.all()

    def put(self, request, pk, format=None):
        user = self.queryset.get(id=pk)
        self.check_object_permissions(self.request, user)
        file_obj = request.data['file']
        user.avatar = file_obj
        user.save()
        return Response(status=204)


class List(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserListSerializer
    permission_classes = (permissions.AllowAny,)