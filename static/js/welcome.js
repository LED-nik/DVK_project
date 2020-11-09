$(document).ready(function () {
    $('.header').height($(window).height());

    $('#logOut').on('click', function () {
        document.cookie = "sid = undefined";

    })
});