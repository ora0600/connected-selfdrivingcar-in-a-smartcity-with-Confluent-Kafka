var mymap = L.map('mapid').setView([50.336, 6.94], 15);
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
       attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
       maxZoom: 18,
       id: 'mapbox/streets-v11',
       tileSize: 512,
       zoomOffset: -1,
       accessToken: 'Please add your token here' //ENTER YOUR TOKEN HERE
      }).addTo(mymap);

mapMarkers1 = [];

var source = new EventSource('/topic/selfdrivingcar'); //ENTER YOUR TOPICNAME HERE
source.addEventListener('message', function(e){

  console.log('Message');
  obj = JSON.parse(e.data);
  console.log(obj);

  if(obj.selfdrivingcar == '000001') {
    for (var i = 0; i < mapMarkers1.length; i++) {
      mymap.removeLayer(mapMarkers1[i]);
    }
    var marker1 = L.marker([obj.longitude,obj.latitude]).addTo(mymap);
    if (obj.latitude == 6.9496495 &&  obj.longitude == 50.3368724) {
      marker1.bindPopup("Das <b>Dorinthotel</b> würde sich über ein Besuch freuen. 20% Discount für Sie!").openPopup();
    } 
    if (obj.latitude == 6.9426784 &&  obj.longitude == 50.3324277) {
      marker1.bindPopup("Business Meeting inkl. Unterkunft und Meeting Package. Buchen Sie Ihr nächstes Meeting bei uns, siehe <b>www.lindner.de</b>").openPopup();
    } 
    
    //
    mapMarkers1.push(marker1);
  }

}, false);