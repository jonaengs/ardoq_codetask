import json
import re
import os
import webbrowser
from datetime import datetime, timedelta
from itertools import count, chain

id_counter = count()
bucket_size = timedelta(minutes=1)

def flatten(iterable):
    return chain.from_iterable(iterable)

def translate(point, start_end): # start_end = "start" | "end"
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
            "start_end": start_end
        },
        "timestamp": point[f"{start_end}ed_at"]
    }

def transform(point):
    return translate(point, "start"), translate(point, "end")

def get_time(point):
    dt = re.split(r'[.|+]', point["timestamp"])[0]  # Discard microseconds/timezone info if there
    return datetime.strptime(dt, r"%Y-%m-%d %H:%M:%S")

def get_bucket_dict(bucket_time):
    # javascript wants its timestamps in ms. timestamp method returns seconds, so multiply by 1000
    return {"timestamp": bucket_time.timestamp() * 1000, "points_list": []}

def into_buckets(points):  # takes transformed and sorted points
    points = iter(points)
    point = next(points)
    current_bucket_time = get_time(point).replace(second=0)
    buckets = [get_bucket_dict(current_bucket_time)]
    while True:
        if get_time(point) - current_bucket_time <= bucket_size:
            buckets[-1]["points_list"].append(point)
            try: point = next(points)
            except: break
        else:
            buckets.append(get_bucket_dict(current_bucket_time))
            current_bucket_time += bucket_size
    
    return buckets 

def to_geojson_ish(fn):
    data = json.load(open(fn, mode="r"))
    transformed = into_buckets(sorted(flatten(map(transform, data)), key=get_time))
    json_str = json.dumps({
        "type": "FeatureCollection", 
        "features": transformed
        })
    final_str = f"data_callback({json_str});"
    open("data/transformed.js", mode="w").write(final_str)

    webbrowser.open('file://' + os.path.realpath("index.html"))


to_geojson_ish("data/07.json")