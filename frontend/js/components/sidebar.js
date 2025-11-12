
class SidebarManager {
    static async load() {
        try {
            console.log('🔄 Cargando sidebar...');
            
            const response = await fetch('/static/templates/sidebar.html');
            if (!response.ok) throw new Error('No se pudo cargar el sidebar');
            
            const html = await response.text();
            document.body.insertAdjacentHTML('afterbegin', html);
            
            this.setupEventListeners();
            console.log('✅ Sidebar cargado correctamente');
            
        } catch (error) {
            console.error('❌ Error cargando sidebar:', error);
            // Fallback silencioso 
        }
    }

    static setupEventListeners() {
        // Mobile menu
        const mobileBtn = document.getElementById('mobileMenuBtn');
        if (mobileBtn) {
            mobileBtn.addEventListener('click', (e) => {
                e.preventDefault();
                // 👇 USA toggleSidebar de tu auth.js si existe
                if (typeof toggleSidebar === 'function') {
                    toggleSidebar();
                    console.log('🎯 Usando toggleSidebar existente de auth.js');
                } else {
                    // Fallback por si acaso
                    this.toggleSidebar();
                }
            });
        }

        // Navegación entre páginas
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const page = item.getAttribute('data-page');
                this.navigateToPage(page);
            });
        });

        // Cerrar sidebar al hacer clic fuera 
        this.setupClickOutside();
    }

    // Función de respaldo (solo se usa si no existe toggleSidebar)
    static toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
            sidebar.classList.toggle('active');
        }
    }

    static navigateToPage(page) {
        console.log('🧭 Navegando a:', page);
        window.location.href = `/${page}`;
    }

    static setActivePage(currentPage) {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        
        const activeItem = document.querySelector(`.nav-item[data-page="${currentPage}"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }
    }

    static setupClickOutside() {
        // Tu código existente en auth.js ya maneja esto
        // No lo duplicamos para evitar conflictos
        console.log('✅ Usando manejo de clics externos de auth.js');
    }
}

// Hacer disponible globalmente
window.SidebarManager = SidebarManager;