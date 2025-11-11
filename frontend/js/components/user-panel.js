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
            
            console.log('✅ User panel cargado correctamente');
            
        } catch (error) {
            console.error('❌ Error cargando user panel:', error);
        }
    }
}

window.UserPanelManager = UserPanelManager;