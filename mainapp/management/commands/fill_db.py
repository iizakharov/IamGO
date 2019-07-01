from django.core.management.base import BaseCommand
from mainapp.models import EventCategory, EventAgent, EventLocation, Event

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
        EventCategory.objects.all().delete()
        category_list = dict()
        for category in categories:
            category_list[category['name']] = category['description']
        [EventCategory.objects.create(name=key, description=value) for key, value in category_list.items()]
        print("Categories created")
        # Create agents
        agents = load_from_json('agents')
        EventAgent.objects.all().delete()
        print("agents loaded")
        agent_list = dict()
        for agent in agents:
            agent_list[agent['name']] = agent['description']
        [EventAgent.objects.create(name=key, description=value) for key, value in agent_list.items()]
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
            print(event['agent'])
            event['agent'] = EventAgent.objects.get(name=event['agent'])
            print(event['agent'])
            event_object = Event.objects.create(**event)
            # print('{0} created.'.format(event['name']))
            for location in locations:
                if event['name'] == location['event']:
                    event_object.location.add(EventLocation.objects.get(name=location['name']))
            for category in categories:
                if event['name'] == category['event']:
                    event_object.category.add(EventCategory.objects.get(name=category['name']))

            # print('{0} is done.'.format(event['name']))

            # category_name = event['category']
            # # Получаем категорию по имени
            # _category = EventCategory.objects.get(name=category_name)
            # _agent = EventAgent.objects.get(name=event['agent'])
            # _location = EventLocation.objects.filter(name=event['location'])
            # _date = event['date']
            # event.pop('location', None)
            # event.pop('date', None)
            # # Заменяем название категории объектом
            # # _event = Event.objects.create(**event)
            # event['category'] = _category
            # event['agent'] = _agent
            # event['date'] = _date
            # # event['location'] = _location
            # event_object = Event.objects.create(**event)
            # event_object.location.set(_location)
