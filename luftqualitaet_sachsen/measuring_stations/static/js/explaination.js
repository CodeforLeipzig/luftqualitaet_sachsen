/**
 * Created by Kater169 on 27.04.15.
 */
$(function() {
    $.get(window.explainationsJsonUrl, function(data) {
        console.log(data);
        data.forEach(function (value, i) {
            var $template = $('#template').clone();
            var control = 'collapse' + i;
            var heading = 'heading' + i;

            $template.find('.panel-title a').html(value.title).attr('href', '#' + control).attr('aria-controls', control);
            $template.find('.panel-heading').attr('id', heading);
            $template.find('.panel-collapse').attr('id', control).attr('headingOne', heading);
            if(i==0) {
                $template.find('.panel-collapse').addClass('in');
            }
            $template.find('.panel-body').html(value.desc);
            $template.removeClass('hidden');

            $('#explain-list').append($template);
        });
    });

});