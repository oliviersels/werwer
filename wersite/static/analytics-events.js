
$( document ).ready(function () {
    $('.moreInfoEvent').on('click', function(e) {
        ga('send', 'Feature Popularity', 'More Info', $(this).data('event-value'))
    });
});
