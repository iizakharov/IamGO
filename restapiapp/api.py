from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.resources import ModelResource
from mainapp.models import Event, EventCategory, EventAgent, EventLocation, EventGallery, EventDate


class EventCategoryResource(ModelResource):
    class Meta:
        queryset = EventCategory.objects.all()
        resource_name = 'category'
        authorization = Authorization()


class EventAgentResource(ModelResource):
    class Meta:
        queryset = EventAgent.objects.all()
        resource_name = 'agent'
        authorization = Authorization()


class EventLocationResource(ModelResource):
    class Meta:
        queryset = EventLocation.objects.all()
        resource_name = 'location'
        authorization = Authorization()


class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all().select_related()
        resource_name = 'event'
        authorization = Authorization()

    category = fields.ManyToManyField(EventCategoryResource, 'category', full=True)
    agent = fields.ForeignKey(EventAgentResource, 'agent', full=True)
    location = fields.ManyToManyField(EventLocationResource, 'location', full=True)


class EventGalleryResource(ModelResource):
    class Meta:
        queryset = EventGallery.objects.all()
        resource_name = 'gallery'
        authorization = Authorization()

    event = fields.ForeignKey(EventResource, 'event', full=True)


class EventDateResource(ModelResource):
    class Meta:
        queryset = EventDate.objects.all()
        resource_name = 'date'
        authorization = Authorization()

    event = fields.ForeignKey(EventResource, 'event', full=True)
