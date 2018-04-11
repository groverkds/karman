$(function () {
    $('.chat-header').click(function () {
        $(this).toggleClass('offline');
        $(this).toggleClass('online');
        $('.chat-window').toggleClass('docked');
    });

    setInterval(function () {
        $('.progress-indicator').toggleClass('hide');
    }, 7846);
});        