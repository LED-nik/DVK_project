$(document).ready(function () {
    $('.header').height($(window).height());

    $('#loginForm').on('submit', () => {
     let login = $('#loginInput').val(),
         password = $('#passwordInput').val();
     alert(`your login is ${login}. And password is ${password}`);
    })


});
