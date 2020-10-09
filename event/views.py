from rest_framework import permissions, generics, views, status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from django.core.exceptions import ObjectDoesNotExist
from . import permissions as custom_permissions
from . import serializers
from .models import Event, DateValidationError
from core.models import User

# Create your views here.


class Create(generics.GenericAPIView, CreateModelMixin):
    serializer_class = serializers.EventCreateSerializer
    permission_classes = (custom_permissions.IsOwner,)
    
    def post(self, request, *args, **kwargs):
        try:
            data = request.data.dict()
            user_id = data.pop('created_by')
            user = User.objects.get(id=user_id)
            self.check_object_permissions(self.request, user)
            event = Event(**data)
            event.created_by = user
            event.save()
            response_data = serializers.EventCreateSerializer(event).data
            response_status = status.HTTP_200_OK

        except AttributeError: # Raised when no fields are given in the request
            response_data = {'detail': 'Missing multiple fields.'}
            response_status = status.HTTP_400_BAD_REQUEST

        except KeyError as ke: # Raised when one field is missing in the request
            response_data = {'detail' : 'Missing field.', 'missing': ke.__str__().strip("'")}
            response_status = status.HTTP_400_BAD_REQUEST
            
        except ValueError as ve: # Raised when field's type doesn't match given value
            response_data = {'detail' : 'Incorrect field or fields.'}
            response_status = status.HTTP_400_BAD_REQUEST

        except ObjectDoesNotExist as oe: # Raised when User object cannot be found
            response_data = {'detail' : 'User not found.'}
            response_status = status.HTTP_400_BAD_REQUEST
            
        except DateValidationError as de: # Raised when start_date field is greater than end_date field
            response_data = {'detail' : de.__str__()}
            response_status = status.HTTP_400_BAD_REQUEST
        
        return Response(data=response_data, status=response_status)



class InvitedToList(views.APIView):
    queryset = Event.objects.all()
    serializer_class = serializers.EventCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        ## Check if user and token matches
        user = User.objects.get(username=request.data['username'])
        if str(user.auth_token) != request.data['token']:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        ## Get events created by user
        created_events = self.queryset.created(user=user)
        
        ## Get events user is invited to
        invited_events = self.queryset.invited_to(user=user)

        ## Merge querysets and filter by day
        filtered_by_day = (created_events | invited_events).future_events(within_days = 120)

        data = serializers.EventCreateSerializer(filtered_by_day, many=True).data

        return Response(data=data, status=status.HTTP_200_OK)



class CreatedList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = serializers.EventCreateSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        ## Check if user and token matches
        user = User.objects.get(username=request.data['username'])
        if str(user.auth_token) != request.data['token']:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        ## Get events created by user
        created_events = self.queryset.created(user=user)

        data = serializers.EventCreateSerializer(created_events, many=True).data

        return Response(data=data, status=status.HTTP_200_OK)
        