// initialize map and set zoom
var mymap = L.map('mapid').setView([39.526, -115.94], 10);

// add tiles
L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZGxpbjE3IiwiYSI6ImNpcmsyMGxudzAwMnlmYm5icXlzYWsxd2IifQ.MUxIcntS8U8rRa41fbPo_Q', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="http://mapbox.com">Mapbox</a>',
    id: 'mapbox.streets'
}).addTo(mymap);

// on click do stuff
function onClick(e) {
    console.log(e.target.feature.properties.owner)
};

// define popup and action for each marker
function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.name) {
        layer.bindPopup('<center>' + feature.properties.name + '<br>' +
                        feature.properties.activity + '<br>' +
                        feature.properties.owner + '</center>').on('click', onClick);
    }

    var greenIcon = new L.Icon({
        iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
        shadowSize: [0,0],
        iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
    });

    var greyIcon = new L.Icon({
        iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-grey.png',
        shadowSize: [0,0],
        iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
    });

    if (feature.properties.activity == 'Inactive') {
        layer.setIcon(greyIcon)
    } else {
        layer.setIcon(greenIcon)
    }

    layer.on('mouseover', function(e) {
        this.openPopup();
    });

    layer.on('mouseout', function(e) {
        this.closePopup();
    });
}

// initialize marker layer
var markers = L.geoJSON(false, {
                onEachFeature: onEachFeature
            }).addTo(mymap);

// load markers based on map bounds
function loadMarkers() {
    var bounds = mymap.getBounds();
    var ne = bounds._northEast;
    var sw = bounds._southWest;

    // make call to get geoJSON of all mines in view
    $.ajax({
        url: 'mines_api',
        data: { 
                minlat : sw.lat,
                minlng : sw.lng,
                maxlat : ne.lat,
                maxlng : ne.lng
            },
        type: "GET",
        async: false,
        dataType: 'json',
        complete: function(data) {
            markers.clearLayers();
            
            markers.addData(data.responseJSON);                            
        }
    })
}

loadMarkers();

// add button to render mines
L.easyButton('fa-refresh', function(){
    loadMarkers();
}).addTo(mymap);

mymap.on('click', onClick_close)

function onClick_close(e) {
	closeNav();
}

/* Set the width of the side navigation to 250px */
function openNav() {
	document.getElementById("mySidenav").style.width = "400px";
	document.getElementById("mapid").style.marginRight = "400px";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
	document.getElementById("mySidenav").style.width = "0";
	document.getElementById("mapid").style.marginRight = "0";
}