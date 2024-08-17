document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('registroForm');
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    }, false);

    // Añadir validación individual de campos al perder el foco
    var campos = form.querySelectorAll('.form-control');
    campos.forEach(function(campo) {
        campo.addEventListener('blur', function() {
            if (!campo.checkValidity()) {
                campo.classList.add('is-invalid');
            } else {
                campo.classList.remove('is-invalid');
                campo.classList.add('is-valid');
            }
        });
    });
});

