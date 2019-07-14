import json
import os
import time

import requests
import tempfile

from django.core import files
from django.core.management.base import BaseCommand
from mainapp.models import EventCategory, EventAgent, EventLocation, Event, EventDate, EventGallery
from authapp.models import User

JSON_PATH = 'mainapp/json'
base_url = 'http://127.0.0.1:8000/api/v1/'
username = 'admin@admin.com'
password = 'password'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


def create_categories():
    # Create categories
    url = base_url + 'categories/'
    categories = load_from_json('categories')
    print("Categories loaded")
    unique_categories = dict()
    for category in categories:
        category.pop('event')
        unique_categories[category['name']] = category
    EventCategory.objects.all().delete()
    for name, category in unique_categories.items():
        request = requests.post(url=url, auth=requests.auth.HTTPBasicAuth(username, password), json=category)
        if request.status_code == 201:
            print(f"{name} created")
        else:
            print(f"{name}: {request.status_code}\t{request.text}")
    print("Categories created")


def create_agents():
    # Create agents
    url = base_url + 'agents/'
    agents = load_from_json('agents')
    print("agents loaded")
    EventAgent.objects.all().delete()
    for agent in agents:
        request = requests.post(url=url, auth=requests.auth.HTTPBasicAuth(username, password), json=agent)
        if request.status_code == 201:
            print(f"{agent['name']} created")
        else:
            print(f"{agent['name']}: {request.status_code}\t{request.text}")
    print("Agents created")


def create_locations():
    # Create locations
    locations = load_from_json('locations')
    print("Locations loaded")
    EventLocation.objects.all().delete()
    location_list = dict()
    for location in locations:
        location_list[location['name']] = location['location']
    [EventLocation.objects.create(name=key, location=value) for key, value in location_list.items()]
    print("Locations created")


def create_events():
    # Create events
    locations = load_from_json('locations')
    categories = load_from_json('categories')
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


def create_dates():
    dates = load_from_json("eventdate")
    print("Dates loaded")
    EventDate.objects.all().delete()
    for i in dates:
        EventDate.objects.create(event=Event.objects.get(name=i["event"]), date=i["date"])
    print("Dates created")


def create_gallery():
    pass


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.all().delete()
        User.objects.create_superuser('django@geekshop.local', 'geekbrains')
        User.objects.create_superuser(username, password)
        create_categories()
        create_agents()
        # create_locations()
        # create_events()
        # create_dates()
        # create_gallery()
        #
        # print("Recreate users: ", end='')
        # User.objects.all().delete()
        # User.objects.create_superuser('django@geekshop.local', 'geekbrains')
        # User.objects.create_superuser("admin@admin.com", "password")
        # print("Done")
