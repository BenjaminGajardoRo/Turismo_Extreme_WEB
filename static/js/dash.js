// dash.js

function showAlert(message, type) {
    // Create alert element
    var alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.role = 'alert';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    // Append alert to the container
    document.getElementById('alert-container').appendChild(alert);

    // Automatically remove the alert after 5 seconds
    setTimeout(() => {
        alert.classList.remove('show');
        alert.classList.add('hide');
        setTimeout(() => alert.remove(), 200);
    }, 5000);
}

function errorAlEliminar() {
    showAlert('Error al eliminar.', 'danger');
}

function eliminadoSatisfactoriamente() {
    showAlert('Eliminado satisfactoriamente.', 'success');
}

function respuestaEnviadaCorrectamente() {
    showAlert('Respuesta enviada correctamente.', 'success');
}

function errorAlEnviarRespuesta() {
    showAlert('Error al enviar respuesta.', 'danger');
}

function quejaEliminadaSatisfactoriamente() {
    showAlert('Queja eliminada satisfactoriamente.', 'success');
}

function errorAlEliminarQueja() {
    showAlert('Error al eliminar queja.', 'danger');
}

function checkURLParams() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('status')) {
        const status = urlParams.get('status');
        switch (status) {
            case 'errorEliminar':
                errorAlEliminar();
                break;
            case 'eliminado':
                eliminadoSatisfactoriamente();
                break;
            case 'respuestaEnviada':
                respuestaEnviadaCorrectamente();
                break;
            case 'errorRespuesta':
                errorAlEnviarRespuesta();
                break;
            case 'quejaEliminada':
                quejaEliminadaSatisfactoriamente();
                break;
            case 'errorQueja':
                errorAlEliminarQueja();
                break;
        }
    }
}

document.addEventListener('DOMContentLoaded', checkURLParams);
