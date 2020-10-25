from rest_framework import serializers
from .models import Event, Invitation


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'created_by', 'title', 'description', 'location', 'start_date', 'end_date')



class InvitationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ('id', 'event', 'receiver')


class InvitationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ('id', 'event', 'will_attend')


class InvitationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ('id', 'receiver', 'event', 'will_attend')