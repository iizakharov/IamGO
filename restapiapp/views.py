from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from restapiapp.serializers import EventSerializer, EventCategorySerializer, EventGallerySerializer
from restapiapp.serializers import EventDateSerializer, EventLocationSerializer, EventAgentSerializer

from mainapp.models import Event, EventCategory, EventGallery, EventDate, EventLocation, EventAgent


# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'events': reverse('events', request=request, format=format),
#         # 'snippets': reverse('snippet-list', request=request, format=format)
#     })


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer


class EventGalleryViewSet(viewsets.ModelViewSet):
    queryset = EventGallery.objects.all()
    serializer_class = EventGallerySerializer


class EventDateViewSet(viewsets.ModelViewSet):
    queryset = EventDate.objects.all()
    serializer_class = EventDateSerializer


class EventLocationViewSet(viewsets.ModelViewSet):
    queryset = EventLocation.objects.all()
    serializer_class = EventLocationSerializer


class EventAgentViewSet(viewsets.ModelViewSet):
    queryset = EventAgent.objects.all()
    serializer_class = EventAgentSerializer