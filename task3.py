import json
import re
import webbrowser
from datetime import datetime, timedelta
from itertools import count, chain

id_counter = count()
bucket_size = timedelta(minutes=1)

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
    points = iter(points)
    point = next(points)
    current_bucket_time = get_time(point).replace(second=0)
    buckets = [{"timestamp": current_bucket_time.timestamp() * 1000, "points_list": []}]
    while True:
        if get_time(point) - current_bucket_time <= bucket_size:
            buckets[-1]["points_list"].append(point)
            try: point = next(points)
            except: break
        else:
            buckets.append({"timestamp": current_bucket_time.timestamp() * 1000, "points_list": []})
            current_bucket_time += bucket_size
    
    return buckets 

def to_geojson(fn):
    with open(fn, mode="r") as f:
        data = json.load(f)
    transformed = into_buckets(sorted(flatmap(transform, data), key=get_time))
    json_str = json.dumps({
        "type": "FeatureCollection", 
        "features": transformed
        })
    with open("data/transformed.js", mode="w") as out:
        out.write("data_callback(" + json_str + ");")

    webbrowser.open('file://' + os.path.realpath(filename))

to_geojson("data/07.json")