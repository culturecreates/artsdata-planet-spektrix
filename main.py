import requests, json, sys, os

source = os.environ.get('SOURCE')

base_url = f"https://system.spektrix.com/{source}/api/v3"

def get_events():
    print("Getting events...")
    response = requests.get(f"{base_url}/events")
    response.raise_for_status()
    return response.json()

def get_venues():
    print("Getting venues...")
    response = requests.get(f"{base_url}/venues")
    response.raise_for_status()
    return response.json()

def get_instances():
    print("Getting instances...")
    response = requests.get(f"{base_url}/instances")
    response.raise_for_status()
    return response.json()

def get_plans():
    print("Getting plans...")
    response = requests.get(f"{base_url}/plans")
    response.raise_for_status()
    return response.json()

def enrich_event_with_location(event, venues, instances, plans):
    print(f"Enriching event {event.get('id')} with location...")
    event_id = event.get("id")
    if not event_id:
        return event

    event_instances = [instance for instance in instances if instance.get("event", {}).get("id") == event_id]
    event['locations'] = [] 

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
    events = get_events()
    venues = get_venues()
    instances = get_instances()
    plans = get_plans()
    enriched_events = [enrich_event_with_location(event, venues, instances, plans) for event in events]

    json_data = json.dumps(enriched_events, indent=4)

    if not os.path.exists("json_data"):
        os.makedirs("json_data")

    with open(f"json_data/{source}.json", "w") as file:
        file.write(json_data)

    print(f"Events have been saved to ${source}.json")

if __name__ == "__main__":
    main()
