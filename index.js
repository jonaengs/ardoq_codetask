let map;

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

const data_callback = function (data) {
    for (feature of data.features) {
        const latLng = new google.maps.LatLng(...feature.geometry.coordinates);
        new google.maps.Marker({position: latLng, map: map});
    }
};
