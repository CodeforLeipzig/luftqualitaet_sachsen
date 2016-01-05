var getMap = function(elm){
  L.mapbox.accessToken = 'pk.eyJ1IjoiY29kZWZvcmxlaXB6aWciLCJhIjoiNThhNzA0ZjVmMTEzN2YxMWYyNDA5MjA1MDhmNmY0N2UifQ.MxrVdeSoW8l1PWaTcKYmvA';
  var map = L.mapbox.map(elm[0], 'codeforleipzig.mn3m572l', {
      zoomControl: false, detectRetina: true}).setView([51.3417825, 12.3936349], 14);

  L.tileLayer('http://{s}.tiles.mapbox.com/v4/codeforleipzig.mn3m572l/{z}/{x}/{y}@2x.png?access_token=pk.eyJ1IjoiY29kZWZvcmxlaXB6aWciLCJhIjoiNThhNzA0ZjVmMTEzN2YxMWYyNDA5MjA1MDhmNmY0N2UifQ.MxrVdeSoW8l1PWaTcKYmvA'
  ).addTo(map);
  return map;
}
