/**
 * Created by Martin Feige <m.feige@me.com> on 12.10.15.
 */
$(function () {
    var colors = d3.scale.category20().range(),
        popupOptions = {keepInView: true, minWidth: 500};

    var getMeasurePoints = function(URLs) {
        var map = getMap($('#start_map'));
        $.get(URLs.measuringpoint_overview, function(res){
            console.log(res);
            for(var i in res){
                var detail = res[i],
                    pos = detail['position'].split(',');
                var elm = getPopup(detail);
                var marker = L.marker(pos).bindPopup(elm);
                marker.addTo(map);

                marker.on('click', (function(){
                    var chart = getChart(detail['csv_url'] + '?limit=1&flat=1', $(elm.getContent()));
                }));

            }
        });
    };

    var getPopup = function(data) {
        var $tpl = $('#marker-template').clone(),
            popup = L.popup(popupOptions);
        $tpl.removeAttr('id', 'marker-template');
        $tpl.removeClass('hidden');
        $tpl.find('.location').html(data['location']);
        $tpl.find('.city').html(data['city']);
        $tpl.find('.amsl').html(data['amsl']);
        $tpl.find('.category').html(data['category']);
        if(data['thumb']) {
            $tpl.find('img').attr('src', data['thumb']).removeClass('hidden');
        }
        popup.setContent($tpl[0]);
        return popup
    };

    var getChart = function(url, $elm){
        var chart = c3.generate({
            bindto: $elm.find('.chart')[0],
            data: {
                url: url,
                x: 'x',
                type: 'bar',
                color: function (color, d) {
                    return colors[d.index];
                },
                labels: true
            },
            axis: {
                rotated: true,
                x: {
                    type: 'category'
                },
                y: {
                    label: {
                        text: 'µg/m³',
                        position: 'outer-center'
                    }
                }
            },
            tooltip: {
                show: false
            },
            size: {
                height: 200,
                width: 300
            },
            legend: {
                show: false
            }
        });
        return chart;
    }

    var init = function(){
        window.getAPIURLs(getMeasurePoints)
    };
    init();
});
