import json
from itertools import count, chain
from pprint import pprint

id_counter = count()

def translate(point, start_end):
    return {
        "dt": point[start_end + "ed_at"],
        "name": point[start_end + "_station_name"], 
        "coordinates": [point[start_end + "_station_longitude"], point[start_end + "_station_latitude"]]
    }

def split(point):
    return translate(point, "start"), translate(point, "end")

def transform(point):
    return {
        "type": "feature",
        "geometry": {
            "type": "Point",
            "coordinates": point["coordinates"] # as list
        },
        "properties": {
            "@id": next(id_counter),
            "time": point["dt"]
        }
    }


def get_time(point):
    dt = point["properties"]["time"]
    return datetime.strptime(dt, r"%Y-%m-%d %H:%M:%S")

            out.write("eqfeed_callback(" + json_str + ");")

def to_geojson(fn):
    with open(fn, mode="r") as f:
        data = json.load(f)
        transformed = sorted(
            map(
                transform, 
                chain.from_iterable(map(split, data)) # flatten the tuples returned by
            ),
            key=get_time)
        json_str = json.dumps({
            "type": "FeatureCollection", "features": list(transformed)
        })
        with open("data/transformed.js", mode="w") as out:
            out.write("eqfeed_callback(" + json_str + ");")


to_geojson("data/sample.json")