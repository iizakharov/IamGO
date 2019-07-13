from django.contrib.auth.models import User, Group
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from restapiapp.serializers import EventSerializer, EventCategorySerializer, EventGallerySerializer
from restapiapp.serializers import EventDateSerializer, EventLocationSerializer, EventAgentSerializer

from mainapp.models import Event, EventCategory, EventGallery, EventDate, EventLocation, EventAgent


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'events': reverse('restapiapp:event-list', request=request, format=format),
        # 'snippets': reverse('snippet-list', request=request, format=format)
    })


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)


class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)


class EventGalleryViewSet(viewsets.ModelViewSet):
    queryset = EventGallery.objects.all()
    serializer_class = EventGallerySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('event',)


class EventDateViewSet(viewsets.ModelViewSet):
    queryset = EventDate.objects.all()
    serializer_class = EventDateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('event',)


class EventLocationViewSet(viewsets.ModelViewSet):
    queryset = EventLocation.objects.all()
    serializer_class = EventLocationSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'location')


class EventAgentViewSet(viewsets.ModelViewSet):
    queryset = EventAgent.objects.all()
    serializer_class = EventAgentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)