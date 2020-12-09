$(document).ready(function () {

    let secure = false; // TODO: убрать

    $('.header').height($(window).height());

    function encrypt(passw, openKey, n) {
        let message = passw.split("");
        let encryptedMessage = [];

        for (let char of message) {
            encryptedMessage.push((BigInt(char.charCodeAt(0)) ** BigInt(openKey)) % BigInt(n));
        }
        console.log(message, encryptedMessage);
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

    $('#logOut').on('click', function () {
        document.cookie = "sid = undefined";
    });

    $('#chatModal').on('shown.bs.modal', function () {
        let $textArea = $('#formControlTextarea');
        $textArea.trigger('focus');
        $('#sendMessage').on('click', () => {
            let message = $textArea.val();
            $('.chat-list').append($(`<li class="out"> \
                                        <div class="chat-img"> \
                                            <img alt="Avtar" src="static/images/avatar6.png"> \
                                        </div> \
                                        <div class="chat-body"> \
                                            <div class="chat-message"> \
                                                <h5>Вы</h5> \
                                                <p>${message}</p> \
                                            </div> \
                                        </div> \
                                    </li>`));
            let encryptedMessage = secure ? encrypt(message, getCookie('open_key'), getCookie('n')) : message; // TODO: удалить
            $.ajax({
                type: 'post',
                url: $('#sendMessage').attr('data-url'),
                data: {'message': encryptedMessage},
                headers: {
                    'custom_csrf_token': getCookie('custom_csrf_token')
                },
                success: function (data) {
                    let answer = data['answer'];
                    $('.chat-list').append($(`<li class="in"> \
                                        <div class="chat-img"> \
                                            <img alt="Avtar" src="static/images/botav.svg"> \
                                        </div> \
                                        <div class="chat-body"> \
                                            <div class="chat-message"> \
                                                <h5>Чат-бот</h5> \
                                                <p  style="font-size: 17px; color: black">${answer}</p> \
                                            </div> \
                                        </div> \
                                    </li>`))
                },
                error: function (data) {
                    alert('error');
                }
            });
        });
    });

    $("#demo-finish").on('click', () => alert("This is a demo version developed for educational purposes. If you are interested in the project, please contact DVAK-Studio."));
});