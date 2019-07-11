from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.resources import ModelResource
from mainapp.models import Event, EventCategory, EventAgent, EventLocation


class EventCategoryResource(ModelResource):
    class Meta:
        queryset = EventCategory.objects.all()
        resource_name = 'category'


class EventAgentResource(ModelResource):
    class Meta:
        queryset = EventAgent.objects.all()
        resource_name = 'agent'


class EventLocationResource(ModelResource):
    class Meta:
        queryset = EventLocation.objects.all()
        resource_name = 'location'


class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
        authorization = Authorization()

    category = fields.ManyToManyField(EventCategoryResource, 'category')
    agent = fields.ForeignKey(EventAgentResource, 'agent')
    location = fields.ManyToManyField(EventLocationResource, 'location')
