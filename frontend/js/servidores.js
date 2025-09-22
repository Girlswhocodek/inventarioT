
document.addEventListener('DOMContentLoaded', function() {
    
    if (window.auth && !window.auth.verificarAutenticacion()) {
        window.location.href = '/login';
        return;
    }
    servidoresUI.inicializar();
});