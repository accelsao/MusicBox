async function getData(url){
    return await fetch(url)
     .then(response => response.json())
     .then(data => {
        return data;
    });
};

function customIcon (opts) {
  return Object.assign({
    path: 'M 0,0 C -2,-20 -10,-22 -10,-30 A 10,10 0 1,1 10,-30 C 10,-22 2,-20 0,0 z M -2,-30 a 2,2 0 1,1 4,0 2,2 0 1,1 -4,0',
    fillColor: '#34495e',
    fillOpacity: 1,
    strokeColor: '#000',
    strokeWeight: 2,
    scale: 1,
  }, opts);
}

var geolocs = []

async function initMap() {
        // six-digit HTML color code
//        var pinColor = "1CECF1";
//        var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
//        new google.maps.Size(21, 34));


        var map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 24.9689352201779, lng: 121.191933011529},
            zoom: 11,
            mapTypeId: 'terrain'
        });

        var stationID = await getData("position.json");

        for (var i = 0; i < stationID.length; i++) {
            var markerPosition = new google.maps.LatLng(stationID[i].lat, stationID[i].lng);
            var marker = new google.maps.Marker({
                position: markerPosition,
                label: {text: i.toString()},
                map: map,
            });
            if (i > 0){
                var polyline = new google.maps.Polygon({
                    paths: [new google.maps.LatLng(stationID[i-1].lat, stationID[i-1].lng), new google.maps.LatLng(stationID[i].lat, stationID[i].lng)],
                    strokeColor: '#FF0000',
                    strokeOpacity: 0.8,
                    strokeWeight: 3,
                    fillColor: '#FF0000',
                    fillOpacity: 0.35,
                    map: map,
                });
            }

        }


        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };
            geolocs.push(pos)
            console.log(geolocs)


          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }

        for (var i = 0; i < geolocs.length; i++) {
             var pos = new google.maps.LatLng(geolocs[i].lat, geolocs[i].lng);
             var marker = new google.maps.Marker({
                position: pos,
                icon: customIcon({
                    fillColor: '#1CECF1'
                }),
                map: map,
             });
             if (i > 0){
                var polyline = new google.maps.Polygon({
                    paths: [new google.maps.LatLng(geolocs[i-1].lat, geolocs[i-1].lng),
                            new google.maps.LatLng(geolocs[i].lat, geolocs[i].lng)],
                    strokeColor: '#FF0000',
                    strokeOpacity: 0.8,
                    strokeWeight: 3,
                    fillColor: '#FF0000',
                    fillOpacity: 0.35,
                    map: map,
                });
            }

        }
        console.log(geolocs)


        setTimeout(initMap, 5000);
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);
      }