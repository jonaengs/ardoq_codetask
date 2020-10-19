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
const num_points_list_count = 10;


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
    let countChart = setupChart();
    let points_count = i = 0;
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
        points_count += points_list.length;
        i++;
        if (i >= num_points_list_count) {
            addData(countChart, timestamp, points_count)
            i = points_count = 0;
        }
        await new Promise(r => setTimeout(r, next_points_interval));
    }
};

function animateCircles(markers) {
    let count = 0;
    let animation_id = window.setInterval(() => {
        count += 1;
        markers.forEach((marker) => 
            marker.set("icon", {...marker.icon, scale: circle_sizes[count]})
        );
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

function setupChart() {
    var ctx = document.getElementById("counts-chart").getContext('2d');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                backgroundColor: 'rgba(220, 120, 160, 0.7)',
                data: []
            }]
        },
        options: {
            title: {
                display: true,
                text: `Number of bikes locked and unlocked during the previous ${num_points_list_count} minutes`,
                fontSize: 14
            },
            legend: {
                display: false
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'series',
                    time: {
                        round: "minute",
                        unit: "minute"
                    }
                }],
                yAxes: [{
                    ticks: {
                        stepSize: 10,
                        precision: 0,
                        suggestedMin: 0,
                        suggestedMax: 60
                    }
                }]
            },
            elements: {
                line: {
                    tension: 0, // disables bezier curves
                }
            }
        }
    });
    return chart;
}

function addData(chart, timestamp, count) {
    let data = chart.data.datasets[0].data;
    data.push({x: new Date(timestamp).getTime(), y: count});
    if (data.length > 12 * 60 / num_points_list_count) { // display up to twelve hours at a time
        data.shift();
    }
    chart.update();
}