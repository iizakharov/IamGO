from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from restapiapp.serializers import EventSerializer

from mainapp.models import Event


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer