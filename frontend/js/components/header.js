// static/js/components/header.js
class HeaderManager {
    static async load(pageTitle, pageIcon = 'fa-home', showButton = false, buttonText = '', buttonAction = '') {
        try {
            console.log('🔄 HeaderManager: Cargando header...');
            
            const response = await fetch('/static/templates/header.html');
            if (!response.ok) throw new Error('No se pudo cargar el header');
            
            const html = await response.text();
            
            // Insertar el template
            const mainContent = document.querySelector('.main-content');
            if (mainContent) {
                mainContent.insertAdjacentHTML('afterbegin', html);
                
                // Configurar dinámicamente
                this.configureHeader(pageTitle, pageIcon, showButton, buttonText, buttonAction);
                
                console.log('✅ HeaderManager: Header cargado y configurado correctamente');
            } else {
                throw new Error('No se encontró .main-content');
            }
            
        } catch (error) {
            console.error('❌ HeaderManager: Error:', error);
        }
    }

    static configureHeader(pageTitle, pageIcon, showButton, buttonText, buttonAction) {
        // Configurar título e ícono
        const titleElement = document.getElementById('header-title');
        const iconElement = document.getElementById('header-icon');
        
        if (titleElement) titleElement.textContent = pageTitle;
        if (iconElement) {
            iconElement.className = `fas ${pageIcon}`;
        }

        // Configurar botón
        const buttonElement = document.getElementById('header-button');
        if (buttonElement) {
            if (showButton) {
                buttonElement.style.display = 'flex';
                const textSpan = document.getElementById('button-text');
                if (textSpan) textSpan.textContent = buttonText;
                
                // Configurar acción del botón
                if (buttonAction) {
                    buttonElement.onclick = function() {
                        eval(buttonAction); // Ejecutar la función
                    };
                }
            } else {
                buttonElement.style.display = 'none';
            }
        }
    }
}

window.HeaderManager = HeaderManager;