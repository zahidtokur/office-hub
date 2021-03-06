from rest_framework import serializers
from .models import Event, Invitation, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'created_by', 'event', 'message', 'created_at')



class EventSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'created_by', 'title', 'description', 'location', 'start_date', 'end_date', 'comments')



class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ('id', 'event', 'receiver', 'will_attend')