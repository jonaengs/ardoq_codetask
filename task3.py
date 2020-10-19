import json
import re
import os
import webbrowser
import argparse
import requests
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



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", "-y", help="year of data recording. Example: 2020", required=True)
    parser.add_argument("--month", "-m", help="month of data recording. Example: 07 (meaning july)", required=True)
    args = parser.parse_args()
    year, month = args.year, args.month
    assert len(year) == 4 and len(month) == 2, "Year must have length 4 and month length 2 (pad with zero on left)"
    assert (int(year) > 2019 or int(month) >= 4) and (int(year) < 2020 or int(month) <= 10),\
        "Can only get data between april 2019 and october 2020"

    filepath = f"data/{year}/{month}.json"
    if not os.path.isfile(filepath):
        if not os.path.exists(f"data/{year}"):
            os.makedirs(f"data/{year}")
        url = f"https://data.urbansharing.com/oslobysykkel.no/trips/v1/{year}/{month}.json"
        print("Data was not found locally. Downloading from:", url)
        r = requests.get(url)
        print("Data download completed.")
        open(filepath, mode="w").write(r.text)
        print("Data saved locally.")
    
    print("Transforming data...")
    to_geojson_ish(filepath)
    print("Data transformed. Displaying in browser...")
    webbrowser.open("file://" + os.path.realpath("index.html"))
