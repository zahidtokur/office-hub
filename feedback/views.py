from rest_framework import permissions, generics, views
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from django.core.exceptions import ObjectDoesNotExist
from . import permissions as custom_permissions
from . import serializers
from .models import Feedback
from core.models import User


class FeedbackList(generics.ListAPIView):
    queryset = Feedback.objects.all()
    permission_classes = (custom_permissions.IsAdmin,)
    serializer_class = serializers.FeedbackSerializer

    def get(self, request):
        self.check_permissions(request)
        response_data = self.serializer_class(self.get_queryset(), many=True).data

        return Response(data=response_data, status=200)



class FeedbackListCategory(generics.ListAPIView):
    queryset = Feedback.objects.all()
    permission_classes = (custom_permissions.IsAdmin,)
    serializer_class = serializers.FeedbackSerializer

    def get(self, request, category):
        self.check_permissions(request)
        response_data = self.serializer_class(self.queryset.filter(category=category), many=True).data

        return Response(data=response_data, status=200)



class FeedbackCreate(views.APIView):
    queryset = Feedback.objects.all()
    permission_classes = (custom_permissions.TokenMatches,)
    serializer_class = serializers.FeedbackSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.dict()
        user_id = data.pop('created_by')
        user = User.objects.get(id=user_id)
        self.check_object_permissions(self.request, user)
        feedback = Feedback(**data)
        feedback.created_by = user
        feedback.save()

        response_data = self.serializer_class(feedback).data

        return Response(response_data, 200)



class FeedbackDelete(views.APIView):
    queryset = Feedback.objects.all()
    permission_classes = (custom_permissions.TokenMatches,)
    serializer_class = serializers.FeedbackSerializer

    def delete(self, request, user_id, feedback_id):
        user = User.objects.get(id=user_id)
        user_feedback = self.queryset.get(id=feedback_id, created_by_id=user_id)
        self.check_object_permissions(self.request, user)
        user_feedback.delete()
        return Response(data={'detail': 'Object deleted.'}, status=200)



class UserFeedbackList(generics.ListAPIView):
    queryset = Feedback.objects.all()
    permission_classes = (custom_permissions.TokenMatches,)
    serializer_class = serializers.FeedbackSerializer

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        self.check_object_permissions(self.request, user)

        response_data = self.serializer_class(self.queryset.filter(created_by=user), many=True).data

        return Response(data=response_data, status=200)