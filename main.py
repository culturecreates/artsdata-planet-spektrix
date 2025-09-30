import requests, json, os, util, yaml, time
from datetime import datetime, timedelta

source = os.environ.get('SOURCE').strip()

base_url = f"https://system.spektrix.com/{source}/api/v3"

def get_entities(entity):
    print(f"Getting {entity}...")
    response = requests.get(f"{base_url}/{entity}")
    response.raise_for_status()
    return response.json()

def get_minimum_price(instance_id, retries=3, backoff=2):
    url = f"{base_url}/instances/{instance_id}/price-list"

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            prices = data.get('prices', [])
            
            return min(
                (price.get('amount', float('inf')) for price in prices if price.get('amount') is not None),
                default=None
            )
        
        except (requests.RequestException, ValueError) as e:
            if attempt < retries:
                time.sleep(backoff ** attempt)
            else:
                print(f"Failed to fetch price list after {retries} attempts: {e}")
                return None

def enrich_event(event, venues, instances, plans, additional_info):
    print(f"Enriching event {event.get('id')} with location...")

    for venue_data in venues:
        venue_data["address"] = util.split_address(venue_data.get('address', ''))           

    event_id = event.get("id")
    if not event_id:
        return event

    event_instances = [instance for instance in instances if instance.get("event", {}).get("id") == event_id]
    event['locations'] = [] 
    event['source'] = source

    if event_instances:
        split_events = []
        for instance in event_instances:
            new_event = dict(event)  
            for key, value in instance.items():
                new_event[f"instance_{key}"] = value
            event_duration = event.get("duration", 0) or 60
            new_event['duration'] = "PT" + str(event_duration) + "M"
            new_event['lastInstanceDateTime'] = (
                datetime.fromisoformat(new_event['firstInstanceDateTime']) + 
                timedelta(minutes=event_duration)
            ).isoformat()
            if new_event.get('attribute_LowestPrice') is None:
                new_event['attribute_LowestPrice'] = get_minimum_price(instance.get('id'))
            new_event = util.add_additional_info(new_event, additional_info)
            
            plan_id = instance.get("planId")
            plan = next((plan for plan in plans if plan.get("id") == plan_id), None)
            venue_id = plan.get("venue", {}).get("id") if plan else None

            new_event['locations'] = []

            if venue_id and not any(location.get("id") == venue_id for location in new_event['locations']):
                venue_info = next((venue for venue in venues if venue.get("id") == venue_id), None)
                if venue_info:
                    new_event['locations'].append(venue_info)

            split_events.append(new_event)

        return split_events

def main():
    try:
        events = get_entities("events")
        venues = get_entities("venues")
        instances = get_entities("instances")
        plans = get_entities("plans")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        exit(0)
    with open("additional_info.yaml") as f:
        additional_info = yaml.safe_load(f)

    additional_info_for_source = additional_info.get(source, {})
    enriched_events = [
        enriched_event
        for event in events
        for enriched_event in enrich_event(event, venues, instances, plans, additional_info_for_source)
    ]

    enriched_events = util.replace_empty_with_null(enriched_events)

    json_data = json.dumps(enriched_events, indent=4)

    if not os.path.exists("json_data"):
        os.makedirs("json_data")

    with open(f"json_data/{source}.json", "w") as file:
        file.write(json_data)

    print(f"Events have been saved to {source}.json")

if __name__ == "__main__":
    main()
