let map;

const base_circle_size = 10;
const num_circle_sizes = 7;
const circle_sizes = Array.from(
    {length: num_circle_sizes - 1}, 
    (_, k) => base_circle_size * (1 - (k**2 / num_circle_sizes**2))
).concat([0]);
const animation_length = 1500;
const animate_interval = animation_length / num_circle_sizes;
const next_points_interval = 250;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 13,
        center: new google.maps.LatLng(59.91529471008158, 10.75179540278025),
        mapTypeId: "roadmap",
    });
    const script = document.createElement("script");
    script.src = 'data/transformed.js';
    document.getElementsByTagName("head")[0].appendChild(script);
}

async function data_callback(data) {
    let i = 0;
    for (points_list of data.features) {
        markers = points_list.map(
            (point) => new google.maps.Marker({
                position: new google.maps.LatLng(...point.geometry.coordinates),
                icon: getCircle(point.properties.start_end),
                map: map
            })
        )
        if (markers) {
            animateCircles(markers, i);
        }
        await new Promise(r => setTimeout(r, next_points_interval));
        i++;
    }
};

function animateCircles(markers, i) {
    let count = 0;
    let animation_id = window.setInterval(() => {
        count += 1;
        markers.forEach((marker) => marker.set("icon", {...marker.icon, scale: circle_sizes[count]}));
        if (count >= num_circle_sizes) {
            console.log("markers:", i, " count:", count);
            markers.forEach((marker) => marker.setMap(null));
            clearInterval(animation_id); 
        }
    }, animate_interval);
}

function getCircle(start_end) {
    return {
      path: google.maps.SymbolPath.CIRCLE,
      fillColor: start_end == "start" ? "green" : "red",
      fillOpacity: 0.5,
      scale: circle_sizes[0],
      strokeColor: "white",
      strokeWeight: 0.5,
    };
}
