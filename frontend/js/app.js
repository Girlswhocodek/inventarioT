// Mostrar resultados de búsqueda
const mostrarResultados = (data) => {
    const resultadosDiv = document.getElementById('resultados');
    if (!resultadosDiv) return;
    
    resultadosDiv.innerHTML = '';
    let totalResults = 0;

    if (data.servidores && data.servidores.length > 0) {
        totalResults += data.servidores.length;
        resultadosDiv.innerHTML += '<h3 style="margin: 20px 0 10px; color: #4361ee;"><i class="fas fa-server"></i> Servidores</h3>' + crearTabla(data.servidores, ['nombre', 'ip', 'estado', 'responsable']);
    }
    
    if (data.sistemas_operativos && data.sistemas_operativos.length > 0) {
        totalResults += data.sistemas_operativos.length;
        resultadosDiv.innerHTML += '<h3 style="margin: 20px 0 10px; color: #4361ee;"><i class="fab fa-windows"></i> Sistemas Operativos</h3>' + crearTabla(data.sistemas_operativos, ['nombre', 'distribucion', 'version']);
    }
    
    if (data.bases_datos && data.bases_datos.length > 0) {
        totalResults += data.bases_datos.length;
        resultadosDiv.innerHTML += '<h3 style="margin: 20px 0 10px; color: #4361ee;"><i class="fas fa-database"></i> Bases de Datos</h3>' + crearTabla(data.bases_datos, ['nombre', 'motor', 'responsable', 'espacio_gb']);
    }
    
    if (data.gestores && data.gestores.length > 0) {
        totalResults += data.gestores.length;
        resultadosDiv.innerHTML += '<h3 style="margin: 20px 0 10px; color: #4361ee;"><i class="fas fa-tools"></i> Gestores</h3>' + crearTabla(data.gestores, ['nombre', 'tipo', 'version']);
    }
    
    const resultCount = document.getElementById('resultCount');
    if (resultCount) {
        resultCount.textContent = totalResults;
    }
    
    if (totalResults === 0) {
        resultadosDiv.innerHTML = '<div style="text-align: center; padding: 40px; color: #666;"><i class="fas fa-search" style="font-size: 48px; margin-bottom: 15px;"></i><p>No se encontraron resultados</p></div>';
    }
};

// Crear tabla de resultados
const crearTabla = (items, campos) => {
    let html = '<table><tr>';
    campos.forEach(campo => html += '<th>' + campo.replace('_', ' ').toUpperCase() + '</th>');
    html += '</tr>';
    
    items.forEach(item => {
        html += '<tr>';
        campos.forEach(campo => {
            let value = item[campo] || 'N/A';
            if (campo === 'estado') {
                let badgeClass = 'badge-success';
                if (value.toLowerCase().includes('inactivo') || value.toLowerCase().includes('mantenimiento')) {
                    badgeClass = 'badge-warning';
                } else if (value.toLowerCase().includes('error') || value.toLowerCase().includes('caido')) {
                    badgeClass = 'badge-danger';
                }
                html += '<td><span class="badge ' + badgeClass + '">' + value + '</span></td>';
            } else {
                html += '<td>' + value + '</td>';
            }
        });
        html += '</tr>';
    });
    
    return html + '</table>';
};

// Función de búsqueda
const buscar = async () => {
    const searchInput = document.getElementById('searchInput');
    const filtroSelect = document.getElementById('filtroSelect');
    
    if (!searchInput || !filtroSelect) return;
    
    const query = searchInput.value;
    const nivel = filtroSelect.value;
    
    try {
        const resultados = await window.api.buscar(query, nivel);
        if (resultados) {
            mostrarResultados(resultados);
        }
    } catch (error) {
        console.error('Error en la búsqueda:', error);
        const resultadosDiv = document.getElementById('resultados');
        if (resultadosDiv) {
            resultadosDiv.innerHTML = '<div style="text-align: center; padding: 40px; color: #666;"><i class="fas fa-exclamation-triangle" style="font-size: 48px; margin-bottom: 15px;"></i><p>Error al realizar la búsqueda</p></div>';
        }
    }
};

// Configurar event listeners
const configurarEventListeners = () => {
    // Búsqueda con Enter
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                buscar();
            }
        });
    }
    
    // Botón de búsqueda
    const searchButton = document.querySelector('.search-bar button');
    if (searchButton) {
        searchButton.addEventListener('click', buscar);
    }
};

// Cargar KPIs
const cargarKPIs = async () => {
    try {
        const data = await window.api.obtenerKPIs();
        if (data) {
            console.log('Datos de KPIs:', data);
            // Aquí puedes actualizar la UI con los KPIs
        }
    } catch (error) {
        console.error('Error cargando KPIs:', error);
    }
};

// Inicializar aplicación
const inicializarApp = () => {
    if (window.auth.verificarAutenticacion()) {
        const userInfo = window.auth.obtenerInfoUsuario();
        if (userInfo) {
            const usernameDisplay = document.getElementById('usernameDisplay');
            if (usernameDisplay) {
                usernameDisplay.textContent = userInfo.username;
            }
        }
        
        window.auth.configurarPanelUsuario();
        configurarEventListeners();
        cargarKPIs();
        buscar(); // Búsqueda inicial
    }
};

// Hacer funciones disponibles globalmente
window.app = {
    buscar,
    mostrarResultados,
    inicializarApp
};

// Iniciar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', inicializarApp);