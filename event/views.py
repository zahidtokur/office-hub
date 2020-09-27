from rest_framework import permissions, generics, views, status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from . import permissions as custom_permissions
from . import serializers
from .models import Event
from core.models import User

# Create your views here.


class Create(generics.GenericAPIView, CreateModelMixin):
    serializer_class = serializers.EventCreateSerializer
    permission_classes = (custom_permissions.IsOwner,)
    
    def post(self, request, *args, **kwargs):
        data = request.data.dict()
        user_id = data.pop('created_by')
        user = User.objects.get(id=user_id)
        self.check_object_permissions(self.request, user)
        event = Event(**data)
        event.created_by = user
        event.save()
        response_data = serializers.EventCreateSerializer(event).data
        return Response(data=response_data, status=status.HTTP_201_CREATED)
