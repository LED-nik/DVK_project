window.onload = function() {
    (function() {
        const inputText = document.querySelectorAll('.auth-form__input');

        inputText.forEach( function(input) {
            input.addEventListener('focus', function() {
                this.classList.add('focus');
                this.parentElement.querySelector('.auth-form__placeholder').classList.add('focus');
            });
            input.addEventListener('blur', function() {
                this.classList.remove('focus');
                if (! this.value) {
                    this.parentElement.querySelector('.auth-form__placeholder').classList.remove('focus');
                }
            });
        });
    })();

    (function() {
        const togglers = document.querySelectorAll('.password-toggler');

        togglers.forEach( function(checkbox) {
            checkbox.addEventListener('change', function() {

                const toggler = this.parentElement,
                      input   = toggler.parentElement.querySelector('.input-password'),
                      icon    = toggler.querySelector('.auth-form__icon');

                if (checkbox.checked) {
                    input.type = 'text';
                    icon.classList.remove('la-eye')
                    icon.classList.add('la-eye-slash');
                }

                else
                {
                    input.type = 'password';
                    icon.classList.remove('la-eye-slash')
                    icon.classList.add('la-eye');
                }
            });
        });
    })();

    (function() {
        const validEmail = 'test@example.com',
              validPassword = 'qwerty123';

        document.body.querySelector('.hint')
                     .innerHTML = `<p>${validEmail}</p><p>${validPassword}</p>`;

        document.forms['form-auth'].addEventListener('submit', function(e) {
            e.preventDefault();

            const answerContainer = this.querySelector('.auth-form__answer'),
                  email = this.elements.email.value,
                  password = this.elements.password.value;

            const placeholders = document.querySelectorAll('.auth-form__placeholder');

            if (email == validEmail && password == validPassword) {
                answerContainer.innerHTML = '<span class="text-success">you\'ve been logged successfully</span>';
            }

            else {
                placeholders.forEach(function(placeholder) {
                    placeholder.classList.remove('focus');
                });
                this.elements.email.value = '';
                this.elements.password.value = '';
                answerContainer.innerHTML = '<span class="text-danger">invalid email or password</span>';
            }
        });
    })();
};