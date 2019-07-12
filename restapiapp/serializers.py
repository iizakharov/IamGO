from rest_framework import serializers

from mainapp.models import Event


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'description', 'body_text')
        # fields = ('url', 'username', 'email', 'groups')
