// Verificar autenticación
const verificarAutenticacion = () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login';
        return false;
    }
    return true;
};

// Obtener información del usuario desde el token
const obtenerInfoUsuario = () => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return {
            username: payload.sub,
            // Agrega más campos si están en el token
        };
    } catch (e) {
        console.error('Error decodificando token:', e);
        return null;
    }
};

// Cerrar sesión
const cerrarSesion = () => {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
};


// Configurar formulario de login
const configurarLogin = () => {
    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;
    
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const errorMessage = document.getElementById('errorMessage');
        
        try {
            const data = await window.api.login(username, password);
            localStorage.setItem('access_token', data.access_token);
            window.location.href = '/dashboard';
        } catch (error) {
            errorMessage.textContent = 'Credenciales incorrectas. Por favor, verifica tus datos.';
        }
    });
};
  


function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            sidebar.classList.toggle('active');
        }

document.addEventListener('click', function(event) {
    const sidebar = document.getElementById('sidebar');
    const menuBtn = document.querySelector('.mobile-menu-btn');
    
    if (window.innerWidth <= 768 && 
        !sidebar.contains(event.target) && 
        !menuBtn.contains(event.target)) {
        sidebar.classList.remove('active');
    }
});
// Exportar funciones
window.auth = {
    verificarAutenticacion,
    obtenerInfoUsuario,
    cerrarSesion,
    toggleSidebar,
    configurarLogin
};