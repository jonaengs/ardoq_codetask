let map;

const base_circle_size = 15;
const num_circle_sizes = 10
const circle_sizes = Array.from(
    {length: num_circle_sizes}, 
    (_, k) => base_circle_size * (1 - (k**2 / num_circle_sizes**2))
);
const animation_length = 1500;
const animate_interval = animation_length / num_circle_sizes;
const next_points_interval = 1000;

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

const data_callback = async function (data) {
    for (points_list of data.features) {
        markers = points_list.map(
            (point) => new google.maps.Marker({
                position: google.maps.LatLng(...point.geometry.coordinates),
                icon: getCircle(),
                map: map
            })
        )
        animateCircles(markers);
        await new Promise(r => setTimeout(r, next_points_interval));
    }
};

async function animateCircles(markers) {
    let i = 0;
    animation_id = window.setInterval(() => {
      i++;
      if (i < num_circle_sizes) {
        markers.forEach((marker) => {marker.set("icon", getCircle(i))});
      }
    }, animate_interval);
    await new Promise(r => setTimeout(r, animation_length));
    clearInterval(animation_id);
    markers.forEach((marker) => marker.setMap(null));
}

function getCircle(circle_size_index=0) {
    return {
      path: google.maps.SymbolPath.CIRCLE,
      fillColor: "red",
      fillOpacity: 0.3,
      scale: circle_sizes[circle_size_index],
      strokeColor: "white",
      strokeWeight: 0.5,
    };
}
