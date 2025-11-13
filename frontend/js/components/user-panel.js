// static/js/components/user-panel.js
class UserPanelManager {
    static async load() {
        try {
            console.log('🔄 Cargando user panel...');
            
            const response = await fetch('/static/templates/user-panel.html');
            if (!response.ok) throw new Error('No se pudo cargar user panel');
            
            const html = await response.text();
            
            // Buscar donde insertar (normalmente en un header)
            const header = document.querySelector('.header');
            if (header) {
                header.insertAdjacentHTML('beforeend', html);
            } else {
                // Fallback: insertar al final del body
                document.body.insertAdjacentHTML('beforeend', html);
            }
            this.setupEventListeners();
            this.updateUserInfo();
            console.log('✅ User panel cargado correctamente');
            
        } catch (error) {
            console.error('❌ Error cargando user panel:', error);
        }
    }
     static setupEventListeners() {
        console.log('🔧 Configurando eventos del user panel...');
        
        const userInfoPanel = document.getElementById('userInfoPanel');
        const logoutButton = document.getElementById('logoutButton');
        
        if (!userInfoPanel) {
            console.warn('⚠️ userInfoPanel no encontrado');
            return;
        }
            userInfoPanel.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleUserPanel();
        });
         document.addEventListener('click', (e) => {
            const userPanel = document.getElementById('userPanel');
            if (userPanel && userPanel.classList.contains('active')) {
                if (!userInfoPanel.contains(e.target)) {
                    this.hideUserPanel();
                }
            }
        });
          // ✅ LOGOUT - USA la función de auth.js
        if (logoutButton) {
            logoutButton.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
                    // ✅ USA la función de auth.js
                    if (window.auth && typeof window.auth.cerrarSesion === 'function') {
                        window.auth.cerrarSesion();
                    } else {
                        // Fallback
                        localStorage.removeItem('access_token');
                        window.location.href = '/login';
                    }
                }
            });
        }

        console.log('✅ Eventos del user panel configurados');
    }
     static toggleUserPanel() {
        const userPanel = document.getElementById('userPanel');
        if (userPanel) {
            userPanel.classList.toggle('active');
        }
    }

    static hideUserPanel() {
        const userPanel = document.getElementById('userPanel');
        if (userPanel) {
            userPanel.classList.remove('active');
        }
    }

    // ✅ ACTUALIZAR información del usuario usando auth.js
    static updateUserInfo() {
        if (window.auth && typeof window.auth.obtenerInfoUsuario === 'function') {
            const userData = window.auth.obtenerInfoUsuario();
            if (userData && userData.username) {
                const usernameDisplay = document.getElementById('usernameDisplay');
                if (usernameDisplay) {
                    usernameDisplay.textContent = userData.username;
                }
            }
        }
    }
}

window.UserPanelManager = UserPanelManager;