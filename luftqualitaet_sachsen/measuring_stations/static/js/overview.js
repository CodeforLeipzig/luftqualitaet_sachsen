/**
 * Created by Martin Feige <m.feige@me.com> on 12.10.15.
 */
$(function () {

    var getMeasurePoints = function(URLs) {
        var map = getMap($('#start_map'));
        $.get(URLs.measuringpoint_overview, function(res){
            console.log(res);
            for(var i in res){
                var pos = res[i]['position'].split(',');
                var m = L.marker(pos).addTo(map);
            }
        })
    };

    var init = function(){
        window.getAPIURLs(getMeasurePoints)
    };
    init();
});
