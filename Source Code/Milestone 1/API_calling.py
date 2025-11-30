!pip install azure-eventhub

import requests
import json
import time
from datetime import datetime, timezone, timedelta
from azure.eventhub import EventHubProducerClient, EventData

# ===== API KEYS =====
OWM_KEY = "your_openweathermap_api_key_here"
TOMTOM_KEY = "your_tomtom_api_key_here"

# ===== Event Hub Connection =====
EVENT_HUB_CONNECTION = "your_event_hub_connection_string_here"
EVENT_HUB_NAME = "your_event_hub_name_here"

# ===== Fixed Cairo Regions =====
CAIRO_REGIONS = {
    "Downtown": (30.0444, 31.2357),
    "Nasr City": (30.0561, 31.3300),
    "New Cairo": (30.0300, 31.4700),
    "Maadi": (29.9620, 31.2769),
    "Heliopolis": (30.1130, 31.3600),
    "Mokattam": (30.0090, 31.2850)
}

# ===== API FUNCTIONS =====

def get_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": OWM_KEY, "units": "metric"}
    return requests.get(url, params=params).json()

def get_traffic_flow(lat, lon):
    url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json"
    params = {"point": f"{lat},{lon}", "unit": "KMPH", "key": TOMTOM_KEY}
    return requests.get(url, params=params).json().get("flowSegmentData", {})

def get_traffic_incidents(lat, lon, km_radius=1):
    delta = km_radius / 111
    bbox = f"{lon-delta},{lat-delta},{lon+delta},{lat+delta}"

    url = "https://api.tomtom.com/traffic/services/5/incidentDetails"
    params = {
        "bbox": bbox,
        "fields": "{incidents{type,properties{iconCategory}}}",
        "key": TOMTOM_KEY
    }
    return requests.get(url, params=params).json().get("incidents", [])



# ===== STREAMING TO EVENT HUB =====

producer = EventHubProducerClient.from_connection_string(
    conn_str=EVENT_HUB_CONNECTION,
    eventhub_name=EVENT_HUB_NAME
)

print("Connected to Azure Event Hub. Streaming real Cairo data every 60 seconds...")

while True:
    try:
        for region, (lat, lon) in CAIRO_REGIONS.items():

            weather = get_weather(lat, lon)
            flow = get_traffic_flow(lat, lon)
            incidents = get_traffic_incidents(lat, lon)

            record = {
                "region": region,
                "lat": lat,
                "lon": lon,
                "timestamp": datetime.utcnow().isoformat(),
                "weather": weather.get("weather", [{}])[0].get("description"),
                "temperature": weather["main"]["temp"],
                "humidity": weather["main"]["humidity"],
                "wind_speed": weather["wind"]["speed"],
                "current_speed": flow.get("currentSpeed"),
                "free_flow_speed": flow.get("freeFlowSpeed"),
                "travel_time": flow.get("currentTravelTime"),
                "incidents_count": len(incidents)
            }

            event_data = EventData(json.dumps(record))
            producer.send_batch([event_data])

            print(f"Sent: {region} | Speed {record['current_speed']} km/h | Incidents {record['incidents_count']}")

        print("Waiting 60 seconds...\n")
        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)
