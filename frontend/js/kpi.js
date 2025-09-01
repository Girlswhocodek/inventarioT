

// Inicializar gráficos
const inicializarGraficos = () => {
    // Performance Chart
    const perfCtx = document.getElementById('performanceChart');
    if (perfCtx) {
        new Chart(perfCtx, {
            type: 'line',
            data: {
                labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
                datasets: [
                    {
                        label: 'Disponibilidad (%)',
                        data: [99.2, 99.5, 99.3, 99.6, 99.4, 99.8, 99.7, 99.6, 99.5, 99.7, 99.8, 99.85],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        fill: true,
                        tension: 0.3
                    },
                    {
                        label: 'Rendimiento (%)',
                        data: [96.5, 97.2, 97.8, 97.5, 98.2, 98.5, 98.3, 98.7, 98.9, 99.1, 99.2, 99.3],
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        fill: true,
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                }
            }
        });
    }
    
    // Distribution Chart
    const distCtx = document.getElementById('distributionChart');
    if (distCtx) {
        new Chart(distCtx, {
            type: 'doughnut',
            data: {
                labels: ['Servidores', 'Bases de Datos', 'Sistemas Operativos', 'Aplicaciones'],
                datasets: [{
                    data: [45, 25, 20, 10],
                    backgroundColor: [
                        '#2563eb',
                        '#10b981',
                        '#f59e0b',
                        '#ef4444'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        });
    }
};

// Configurar filtros de tiempo
const configurarFiltrosTiempo = () => {
    const timeButtons = document.querySelectorAll('.time-btn');
    
    timeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remover clase active de todos los botones
            timeButtons.forEach(btn => btn.classList.remove('active'));
            
            // Agregar clase active al botón clickeado
            this.classList.add('active');
            
            // Aquí puedes agregar la lógica para filtrar por tiempo
            const periodo = this.textContent.toLowerCase();
            console.log('Filtrando por:', periodo);
            // actualizarKPIs(periodo);
        });
    });
};

// Cargar datos de KPIs desde la API
const cargarDatosKPIs = async () => {
    try {
        const datos = await window.api.obtenerKPIs();
        if (datos) {
            actualizarKPIsUI(datos);
        }
    } catch (error) {
        console.error('Error cargando datos de KPIs:', error);
    }
};

// Actualizar la UI con los datos de KPIs
const actualizarKPIsUI = (datos) => {
    // Aquí puedes actualizar los valores de las tarjetas KPI
    // con los datos reales de la API
    console.log('Datos de KPIs recibidos:', datos);
    
    // Ejemplo:
    // document.querySelector('.kpi-card:nth-child(1) .kpi-value').textContent = datos.disponibilidad + '%';
    // document.querySelector('.kpi-card:nth-child(2) .kpi-value').textContent = datos.incidentes_resueltos + '%';
};

// Configurar event listeners
const configurarEventListeners = () => {
    configurarFiltrosTiempo();
};

// Inicializar página de KPIs
const inicializarPaginaKPIs = () => {
    if (window.auth.verificarAutenticacion()) {
        console.log('Inicializando página de KPIs...');
        configurarEventListeners();
        inicializarGraficos();
        cargarDatosKPIs();
    }
};

// Iniciar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inicializarPaginaKPIs);
} else {
    inicializarPaginaKPIs();
}