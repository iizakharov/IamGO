import json
import csv


def get_events(input, output):
    with open(input) as f:
        reader = csv.DictReader(f, fieldnames=('agent', 'name', 'description', 'body_text', 'price', 'is_free', 'is_active'),
                                delimiter=';')
        out = json.dumps([row for row in reader], ensure_ascii=False, indent=4)
    with open(output, 'w') as f:
        f.write(out)


def get_categories(input, output):
    with open(input) as f:
        reader = csv.DictReader(f, fieldnames=('event', 'name', 'description', 'is_active'),
                                delimiter=';')
        out = json.dumps([row for row in reader], ensure_ascii=False, indent=4)
    with open(output, 'w') as f:
        f.write(out)


def get_locations(input, output):
    with open(input) as f:
        reader = csv.DictReader(f, fieldnames=('event', 'name', 'location'),
                                delimiter=';')
        out = json.dumps([row for row in reader], ensure_ascii=False, indent=4)
    with open(output, 'w') as f:
        f.write(out)


def get_agents(input, output):
    with open(input) as f:
        reader = csv.DictReader(f, fieldnames=('name', 'description', 'is_active'),
                                delimiter=';')
        out = json.dumps([row for row in reader], ensure_ascii=False, indent=4)
    with open(output, 'w') as f:
        f.write(out)


def get_gallery(input, output):
    with open(input) as f:
        reader = csv.DictReader(f, fieldnames=('event', 'image'),
                                delimiter=';')
        out = json.dumps([row for row in reader], ensure_ascii=False, indent=4)
    with open(output, 'w') as f:
        f.write(out)


def get_dates(input, output):
    with open(input) as f:
        reader = csv.DictReader(f, fieldnames=('event', 'date'),
                                delimiter=';')
        out = json.dumps([row for row in reader], ensure_ascii=False, indent=4)
    with open(output, 'w') as f:
        f.write(out)


if __name__ == '__main__':
    get_events("events.csv", "../../json/events.json")
    get_categories("eventcategory.csv", "../../json/categories.json")
    get_locations("location.csv", "../../json/locations.json")
    get_agents("agents.csv", "../../json/agents.json")
    get_gallery("eventgallery.csv", "../../json/eventgallery.json")
    get_dates("eventdate.csv", "../../json/eventdate.json")
