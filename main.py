import requests, json, os

source = os.environ.get('SOURCE').strip()

base_url = f"https://system.spektrix.com/{source}/api/v3"

def get_entities(entity):
    print(f"Getting {entity}...")
    response = requests.get(f"{base_url}/{entity}")
    response.raise_for_status()
    return response.json()

def enrich_event_with_location(event, venues, instances, plans):
    print(f"Enriching event {event.get('id')} with location...")
    event_id = event.get("id")
    if not event_id:
        return event

    event_instances = [instance for instance in instances if instance.get("event", {}).get("id") == event_id]
    event['locations'] = [] 
    event['source'] = source

    if event_instances:
        for instance in event_instances:
            plan_id = instance.get("planId")
            plan = next((plan for plan in plans if plan.get("id") == plan_id), None)
            venue_id = plan.get("venue", {}).get("id")
            if any(location.get("id") == venue_id for location in event['locations']):
                continue
            venue_info = next((venue for venue in venues if venue.get("id") == venue_id), None)
            event['locations'].append(venue_info) 
        return event

def main():
    try:
        events = get_entities("events")
        venues = get_entities("venues")
        instances = get_entities("instances")
        plans = get_entities("plans")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        exit(0)
    enriched_events = [enrich_event_with_location(event, venues, instances, plans) for event in events]

    json_data = json.dumps(enriched_events, indent=4)

    if not os.path.exists("json_data"):
        os.makedirs("json_data")

    with open(f"json_data/{source}.json", "w") as file:
        file.write(json_data)

    print(f"Events have been saved to ${source}.json")

if __name__ == "__main__":
    main()
