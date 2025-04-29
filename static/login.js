document.addEventListener('DOMContentLoaded', function() {
    function setupPasswordToggle(toggleId, fieldId, iconId) {
        const toggle = document.querySelector(toggleId);
        const field = document.querySelector(fieldId);
        const icon = document.querySelector(iconId);
        if (toggle && field && icon) {
            toggle.addEventListener('click', function() {
                const type = field.getAttribute('type') === 'password' ? 'text' : 'password';
                field.setAttribute('type', type);

                icon.classList.toggle('bi-eye');
                icon.classList.toggle('bi-eye-slash');
            });
        }
    }
    setupPasswordToggle('#togglePassword', '#passwordField', '#passwordIcon');
});