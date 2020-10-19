let map;

const base_circle_size = 8;
const num_circle_sizes = 8;
const circle_sizes = Array.from(
    {length: num_circle_sizes - 1}, 
    (_, k) => base_circle_size * (1 - (k**2 / num_circle_sizes**2))
).concat([0]);
const animation_length = 1000;
const update_animation_interval = animation_length / num_circle_sizes;
const next_points_interval = 120;


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
    let dtSpan = document.getElementById("datetime-span");
    for ({timestamp, points_list} of data.features) {
        markers = points_list.map(
            (point) => new google.maps.Marker({
                position: new google.maps.LatLng(...point.geometry.coordinates),
                icon: getCircle(point.properties.start_end),
                map: map
            })
        )
        dtSpan.innerText = new Date(timestamp);
        if (markers) {
            animateCircles(markers);
        }
        await new Promise(r => setTimeout(r, next_points_interval));
    }
};

function animateCircles(markers) {
    let count = 0;
    let animation_id = window.setInterval(() => {
        count += 1;
        markers.forEach((marker) => marker.set("icon", {...marker.icon, scale: circle_sizes[count]}));
        if (count >= num_circle_sizes) {
            markers.forEach((marker) => marker.setMap(null));
            clearInterval(animation_id); 
        }
    }, update_animation_interval);
}

function getCircle(start_end) {
    return {
      path: google.maps.SymbolPath.CIRCLE,
      fillColor: start_end == "start" ? "green" : "red",
      fillOpacity: 0.25,
      scale: circle_sizes[0],
      strokeColor: "white",
      strokeWeight: 0.5,
    };
}
