from django.core.management.base import BaseCommand
from mainapp.models import EventCategory, EventAgent, EventLocation, Event
from authapp.models import User

import json
import os

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create categories
        categories = load_from_json('categories')
        print("Categories loaded")
        EventCategory.objects.all().delete()
        category_list = dict()
        for category in categories:
            category_list[category['name']] = category['description']
        [EventCategory.objects.create(name=key, description=value) for key, value in category_list.items()]
        print("Categories created")
        # Create agents
        agents = load_from_json('agents')
        print("agents loaded")
        EventAgent.objects.all().delete()
        agent_list = dict()
        for agent in agents:
            agent_list[agent['name']] = agent['description']
        [EventAgent.objects.create(name=key, description=value) for key, value in agent_list.items()]
        print("Agents created")
        # Create locations
        locations = load_from_json('locations')
        print("Locations loaded")
        EventLocation.objects.all().delete()
        location_list = dict()
        for location in locations:
            location_list[location['name']] = location['location']
        [EventLocation.objects.create(name=key, location=value) for key, value in location_list.items()]
        print("Locations created")
        # Create events
        events = load_from_json('events')
        print("Events loaded")
        Event.objects.all().delete()
        for event in events:
            # Create event
            event['agent'] = EventAgent.objects.get(name=event['agent'])
            event_object = Event.objects.create(**event)
            # print('{0} created.'.format(event['name']))
            # Add locations to event
            for location in locations:
                if event['name'] == location['event']:
                    event_object.location.add(EventLocation.objects.get(name=location['name']))
            # Add categories to event
            for category in categories:
                if event['name'] == category['event']:
                    event_object.category.add(EventCategory.objects.get(name=category['name']))

            # print('{0} is done.'.format(event['name']))
        print("Events created")
        User.objects.all().delete()
        User.objects.create_superuser('django@geekshop.local', 'geekbrains')
        User.objects.create_superuser("admin@admin.com", "password")
