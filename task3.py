import json
import re
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

def translate(point, start_end, pid): # start_end = "start" | "end"
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                point[f"{start_end}_station_latitude"],
                point[f"{start_end}_station_longitude"]
            ]
        },
        "properties": {
            "@id": pid,
            "start_end": start_end
        },
        "timestamp": point[f"{start_end}ed_at"]
    }

def transform(point):
    pid = next(id_counter)
    return translate(point, "start", pid), translate(point, "end", pid)

def get_time(point):
    dt = re.split(r'[.|+]', point["timestamp"])[0] # Discard microseconds/timezone info if there
    return datetime.strptime(dt, r"%Y-%m-%d %H:%M:%S") # requires python3.7 or greater

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
        transformed = flatmap(transform, data)
        json_str = json.dumps({
            "type": "FeatureCollection", 
            "features": into_buckets(sorted(transformed, key=get_time))
            })
        with open("data/transformed.js", mode="w") as out:
            out.write("data_callback(" + json_str + ");")

to_geojson("data/07.json")