from rest_framework import serializers

from mainapp.models import Event, EventCategory, EventGallery, EventDate, EventLocation, EventAgent


class EventSerializer(serializers.ModelSerializer):
    # gallery = serializers.ReadOnlyField(source='EventGallery.id')
    images = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='restapiapp:eventgallery-detail')
    category = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                   view_name='restapiapp:eventcategory-detail')
    location = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                   view_name='restapiapp:eventlocation-detail')
    dates = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='restapiapp:eventdate-detail')
    # agent = serializers.HyperlinkedRelatedField(many=False, read_only=False, view_name='restapiapp:eventagent-detail')

    class Meta:
        model = Event
        fields = '__all__'


class EventCategorySerializer(serializers.ModelSerializer):
    # event = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = EventCategory
        fields = '__all__'


class EventGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventGallery
        fields = ('__all__')
        read_only_fields = ['image']


class EventGalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventGallery
        fields = ['image']


class EventDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDate
        fields = ('__all__')


class EventLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLocation
        fields = ('__all__')


class EventAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAgent
        fields = ('__all__')