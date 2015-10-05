var getMap = function(elm){
  var map = L.map(elm, {});
  L.tileLayer('http://{s}.tiles.mapbox.com/v4/codeforleipzig.mn3m572l/{z}/{x}/{y}@2x.png?access_token=pk.eyJ1IjoiY29kZWZvcmxlaXB6aWciLCJhIjoiNThhNzA0ZjVmMTEzN2YxMWYyNDA5MjA1MDhmNmY0N2UifQ.MxrVdeSoW8l1PWaTcKYmvA', {
      detectRetina: true,
      attribution: '<a href="https://www.mapbox.com/about/maps/" ' +
      'target="_blank">&copy; Mapbox &copy; OpenStreetMap</a> ' +
      '<a class="mapbox-improve-map" href="https://www.mapbox.com/map-feedback/" ' +
      'target="_blank">Improve this map</a>'
    }).addTo(map);
  return map;
}