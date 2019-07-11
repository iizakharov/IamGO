from tastypie.resources import ModelResource
from mainapp.models import Event


class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'