import json
from datetime import datetime, timedelta
from itertools import count, chain
from pprint import pprint

id_counter = count()

"""
Endring: Del alle punkter i bøtter per 5-minuttersintervaller
Da kan vi gå gjennom hver liste/bøtte, animere alle punktene, 
og gå videre med konstant tid
"""

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
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": point["coordinates"]
        },
        "properties": {
            "@id": next(id_counter)
        },
        "timestamp": point["dt"]
    }

def get_time(point):
    dt = point["timestamp"]
    return datetime.strptime(dt, r"%Y-%m-%d %H:%M:%S.%f%z") # requires python3.7 or greater

def into_buckets(points): # takes transformed and sorted points
    delta = timedelta(minutes=1) # size of each bucket
    buckets = [[]]
    points = iter(points)
    point = next(points)
    current_bucket_time = get_time(point)
    while True:
        if get_time(point) - current_bucket_time <= delta:
            buckets[-1].append(point)
            try: point = next(points)
            except: break
        else:
            buckets.append([])
            current_bucket_time += delta
    
    return buckets
            

def to_geojson(fn):
    with open(fn, mode="r") as f:
        data = json.load(f)
        transformed = map(transform, flatmap(split, data))
        json_str = json.dumps({
            "type": "FeatureCollection", 
            "features": into_buckets(sorted(transformed, key=get_time))
            })
        with open("data/transformed.js", mode="w") as out:
            out.write("data_callback(" + json_str + ");")

to_geojson("data/sample.json")