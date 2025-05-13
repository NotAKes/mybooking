document.addEventListener('DOMContentLoaded', function() {
    function setupPasswordToggle(fieldId, buttonId, iconId) {
        const toggle = document.getElementById(buttonId);
        const field = document.getElementById(fieldId);
        const icon = document.getElementById(iconId);
        if (toggle && field && icon) {
            toggle.addEventListener('click', function() {
                const type = field.getAttribute('type') === 'password' ? 'text' : 'password';
                field.setAttribute('type', type);

                icon.classList.toggle('bi-eye');
                icon.classList.toggle('bi-eye-slash');
            });
        }
    }
    setupPasswordToggle('currentPassword', 'toggleCurrentPassword', 'currentPasswordIcon');
    setupPasswordToggle('newPassword', 'toggleNewPassword', 'newPasswordIcon');
    setupPasswordToggle('repeatPassword', 'toggleRepeatPassword', 'repeatPasswordIcon');
});