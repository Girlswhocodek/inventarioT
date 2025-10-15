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
 try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            document.getElementById('usernameDisplay').textContent = payload.sub;
        } catch (e) {
            console.error('Error decoding token:', e);
        }
document.getElementById('userInfoPanel').addEventListener('click', function(e) {
            e.stopPropagation();
            document.getElementById('userPanel').classList.toggle('active');
        });

        // Cerrar el panel al hacer clic fuera
        document.addEventListener('click', function(e) {
            if (!e.target.closest('#userInfoPanel')) {
                document.getElementById('userPanel').classList.remove('active');
            }
        });
 document.getElementById('logoutButton').addEventListener('click', function() {
            localStorage.removeItem('access_token');
            window.location.href = '/login';
        });

// Configurar panel de usuario
const configurarPanelUsuario = () => {
    const userInfoPanel = document.getElementById('userInfoPanel');
    const userPanel = document.getElementById('userPanel');
    const logoutButton = document.getElementById('logoutButton');
    
    if (!userInfoPanel || !userPanel || !logoutButton) return;
    
    // Toggle del panel
    
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            sidebar.classList.toggle('active');
        }
    
        // Cerrar panel al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!e.target.closest('#userInfoPanel')) {
            userPanel.classList.remove('active');
        }
    });
    
    // Cerrar sesión
    logoutButton.addEventListener('click', function(e) {
        e.preventDefault();
        if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
            cerrarSesion();
        }
    });
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

// Exportar funciones
window.auth = {
    verificarAutenticacion,
    obtenerInfoUsuario,
    cerrarSesion,
    configurarPanelUsuario,
    configurarLogin
};
