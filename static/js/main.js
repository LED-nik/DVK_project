$(document).ready(function () {

    let secure = false; // TODO: убрать

    const $loginForm = $('#loginForm'),
        $userCreateForm = $('#userCreateForm');

    $('.header').height($(window).height());

    function encrypt(passw, openKey, n) {
        let message = passw.split("");
        let encryptedMessage = [];

        for (let char of message) {
            encryptedMessage.push((BigInt(char.charCodeAt(0)) ** BigInt(openKey)) % BigInt(n));
        }
        return encryptedMessage.join("O")
    }

    function getCookie(name) {
        var cookieValue = null;

        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + '=') {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }

        return cookieValue;
    }

    function setCookie(cookieName, value) {
        document.cookie = `${cookieName} = ${value}; max-age=99999`;
    }


    $userCreateForm.submit(function (e) {
        e.preventDefault();
        const $passwordInput = $('input[name="password"]');
        const encryptedPass = secure ? encrypt($passwordInput.val(), getCookie('open_key'), getCookie('n')) : $passwordInput.val(); //TODO:убрать
        let data = $(this).serializeArray();
        data[1]['value'] = encryptedPass;
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'post',
            data: $(this).serialize(),
            headers: {
                'custom_csrf_token': getCookie('custom_csrf_token')
            },
            success: function () {
                alert('Пользователь создан!');
            },
            error(data) {
                alert(data.responseText);
            }
        });
    });

    $loginForm.submit(function (e) {
        e.preventDefault();
        let data = {};
        if (getCookie('sid') === "undefined" || !getCookie('sid')) {
            let encryptedPass = secure ? encrypt($(this).find('input[name="password"]').val(), getCookie('open_key'), getCookie('n')) : $(this).find('input[name="password"]').val(); //TODO: убрать
            data = $(this).serializeArray();
            data[1]['value'] = encryptedPass;
        }
        $.ajax({
            type: 'post',
            url: $(this).attr('data-url'),
            data: data,
            headers: {
                'custom_csrf_token': getCookie('custom_csrf_token')
            },
            success: function (data) {
                setCookie('sid', data['sid']);
                window.location.href = data['redirect_url'];
            },
            error: function (data) {
                alert(data.responseJSON['message']);
            }
        });
    });

});
