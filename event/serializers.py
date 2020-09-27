from rest_framework import serializers
from .models import Event


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'created_by', 'title', 'description', 'location', 'start_date', 'end_date')
