import json
from datetime import datetime
from itertools import count, chain
from pprint import pprint

id_counter = count()

def flatmap(f, iterable):
    return chain.from_iterable(map(f, iterable))

def translate(point, start_end): # start_end = "start" | "end"
    return {
        "dt": point[f"{start_end}ed_at"],
        "name": point[f"{start_end}_station_name"], 
        "coordinates": [
            point[f"{start_end}_station_latitude"], 
            point[f"{start_end}_station_longitude"]
        ]
    }

def split(point):
    return translate(point, "start"), translate(point, "end")

def transform(point):
    return {
        "type": "feature",
        "geometry": {
            "type": "Point",
            "coordinates": point["coordinates"] # [lat, lon] for enkel google.maps.LatLng input
        },
        "properties": {
            "@id": next(id_counter),
            "time": point["dt"]
        }
    }

def get_time(point):
    dt = point["properties"]["time"]
    return datetime.strptime(dt, r"%Y-%m-%d %H:%M:%S.%f%z") # requires python3.7 or greater

def to_geojson(fn):
    with open(fn, mode="r") as f:
        data = json.load(f)
        transformed = map(transform, flatmap(split, data))
        json_str = json.dumps({
            "type": "FeatureCollection", 
            "features": sorted(transformed, key=get_time)
            })
        with open("data/transformed.js", mode="w") as out:
            out.write("data_callback(" + json_str + ");")

to_geojson("data/sample.json")