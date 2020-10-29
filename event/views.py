from rest_framework import permissions, generics, views
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from django.core.exceptions import ObjectDoesNotExist
from . import permissions as custom_permissions
from . import serializers
from .models import Event, Invitation, Comment, DateValidationError
from core.models import User

# Create your views here.


class EventCreate(generics.GenericAPIView, CreateModelMixin):
    serializer_class = serializers.EventSerializer
    permission_classes = (custom_permissions.TokenMatches,)
    
    def post(self, request, *args, **kwargs):
        try:
            data = request.data.dict()
            user_id = data.pop('created_by')
            user = User.objects.get(id=user_id)
            self.check_object_permissions(self.request, user)
            event = Event(**data)
            event.created_by = user
            event.save()
            response_data = serializers.EventSerializer(event).data
            response_status = 200

        except AttributeError: # Raised when no fields are given in the request
            response_data = {'detail': 'Missing multiple fields.'}
            response_status = 400

        except KeyError as ke: # Raised when one field is missing in the request
            response_data = {'detail' : 'Missing field.', 'missing': ke.__str__().strip("'")}
            response_status = 400
            
        except ValueError as ve: # Raised when field's type doesn't match given value
            response_data = {'detail' : 'Incorrect field or fields.'}
            response_status = 400

        except ObjectDoesNotExist as oe: # Raised when User object cannot be found
            response_data = {'detail' : 'User not found.'}
            response_status = 400
            
        except DateValidationError as de: # Raised when start_date field is greater than end_date field
            response_data = {'detail' : de.__str__()}
            response_status = 400
        
        return Response(data=response_data, status=response_status)


class EventUpdate(views.APIView):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = (custom_permissions.TokenMatches,)
    
    def put(self, request, id):
        event = self.queryset.get(id=id)
        self.check_object_permissions(self.request, event.created_by)
        
        data = request.data.dict()

        if "title" in data:
            event.title = data['title']

        if "description" in data:
            event.description = data['description']

        if "location" in data:
            event.location = data['location']

        if "start_date" in data:
            event.start_date = data['start_date']

        if "end_date" in data:
            event.end_date = data['end_date']

        event.save()
        response_data = self.serializer_class(event).data
        return Response(response_data, 200)


class InvitedEventsList(views.APIView):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = (custom_permissions.TokenMatches,)

    def get(self, request, user_id):
        try:
            days = int(request.data['days'])
        except KeyError: # Raised when 'days' value is not provided
            days = 120
        except ValueError: # Raised when 'days' value is not a number
            return Response(data={'detail': 'days must be an integer.'}, status=400)

        ## Check if user and token matches
        user = User.objects.get(id=user_id)
        self.check_object_permissions(request, user)

        ## Get events created by user
        created_events = self.queryset.created(user=user)
        
        ## Get events user is invited to
        invited_events = self.queryset.invited_to(user=user)

        ## Merge querysets and filter by day
        filtered_by_day = (created_events | invited_events).future_events(within_days = days)

        response_data = serializers.EventCreateSerializer(filtered_by_day, many=True).data

        return Response(data=response_data, status=200)



class CreatedEventsList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = (permissions.AllowAny, )

    def get(self, request, user_id):
        ## Check if user and token matches
        user = User.objects.get(id=user_id)
        self.check_object_permissions(request, user)

        ## Get events created by user
        created_events = self.queryset.created(user=user)

        response_data = serializers.EventCreateSerializer(created_events, many=True).data

        return Response(data=response_data, status=200)
        


class InvitationCreate(views.APIView):
    queryset = Invitation.objects.all()
    serializer_class = serializers.InvitationSerializer
    permission_classes = (custom_permissions.TokenMatches,)

    def post(self, request, event_id):
        ## Check if user and token matches
        event = Event.objects.get(id=event_id)
        self.check_object_permissions(request, event.created_by)
        
        for receiver_id in request.data['receiver_ids']:
            inv = Invitation(receiver_id=receiver_id, event=event)
            inv.save()

        response_data = self.serializer_class(event.invitations, many=True).data

        return Response(data=response_data, status=200)




class InvitationUpdate(views.APIView):
    queryset = Invitation.objects.all()
    serializer_class = serializers.InvitationSerializer
    permission_classes = (custom_permissions.TokenMatches,)

    def put(self, request, invitation_id):
        ## Check if user and token matches
        invitation = Invitation.objects.get(id=invitation_id)
        self.check_object_permissions(request, invitation.receiver)

        invitation.will_attend = request.data['will_attend']
        invitation.save()

        response_data = self.serializer_class(invitation).data

        return Response(data=response_data, status=200)



class InvitationList(generics.ListAPIView):
    queryset = Invitation.objects.all()
    serializer_class = serializers.InvitationSerializer
    permissions_classes = (permissions.AllowAny,)

    def get(self, request):
        # Get user
        try:
            token = request.headers['Authorization']
            user = User.objects.get(auth_token=token)
            invitations = self.queryset.filter(receiver=user)
            response_data = self.serializer_class(invitations, many=True).data
            response_status = 200
        except KeyError:
            response_data = {'detail': 'Authentication credentials were not provided.'}
            response_status = 400
        
        return Response(response_data, response_status)


class RespondedInvitationList(generics.ListAPIView):
    queryset = Invitation.objects.all()
    serializer_class = serializers.InvitationSerializer
    permissions_classes = (permissions.AllowAny,)

    def get(self, request):
        # Get user
        try:
            token = request.headers['Authorization']
            user = User.objects.get(auth_token=token)
            invitations = self.queryset.filter(receiver=user, will_attend__isnull=False)
            response_data = self.serializer_class(invitations, many=True).data
            response_status = 200
        except KeyError:
            response_data = {'detail': 'Authentication credentials were not provided.'}
            response_status = 400

        return Response(response_data, response_status)



class PendingInvitationList(generics.ListAPIView):
    queryset = Invitation.objects.all()
    serializer_class = serializers.InvitationSerializer
    permissions_classes = (permissions.AllowAny,)

    def get(self, request):
        # Get user
        try:
            token = request.headers['Authorization']
            user = User.objects.get(auth_token=token)
            invitations = self.queryset.filter(receiver=user, will_attend__isnull=True)
            response_data = self.serializer_class(invitations, many=True).data
            response_status = 200
        except KeyError:
            response_data = {'detail': 'Authentication credentials were not provided.'}
            response_status = 400

        return Response(response_data, response_status)


class CommentCreate(views.APIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = (custom_permissions.TokenMatches,)

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)

        data = request.data.dict()
        user_id = data.pop('created_by')
        user = User.objects.get(id=user_id)
        self.check_object_permissions(request, user)

        comment = Comment(**data)
        comment.event = event
        comment.created_by = user
        comment.save()

        response_data = self.serializer_class(comment).data

        return Response(response_data, 200)


class CommentDetail(views.APIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = (custom_permissions.TokenMatches,)

    def get(self, request, event_id, comment_id):
        event = Event.objects.get(id=event_id)
        comment = Comment.objects.get(id=comment_id)
        token = request.headers['Authorization']
        user = User.objects.get(auth_token=token)
        self.check_object_permissions(request, user)

        if event.invitations.filter(receiver=user) == 0:
            return Response(400)

        response_data = self.serializer_class(comment).data

        return Response(response_data, 200)


class EventCommentList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (custom_permissions.TokenMatches,)

    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)
        token = request.headers['Authorization']
        user = User.objects.get(auth_token=token)
        self.check_object_permissions(request, user)

        if event.invitations.filter(receiver=user) == 0:
            return Response(400)

        response_data = self.serializer_class(event.comments, many=True).data

        return Response(response_data, 200)


class CommentDelete(views.APIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (custom_permissions.TokenMatches,)

    def delete(self, request, event_id, comment_id):
        comment = self.queryset.get(id=comment_id)
        self.check_object_permissions(self.request, comment.created_by)
        comment.delete()
        return Response(data={'detail': 'Object deleted.'}, status=200)