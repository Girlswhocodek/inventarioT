

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
    labels: ['Servidores', 'Bases de Datos', 'Sistemas Operativos', 'Gestores'],
    datasets: [{
        data: [
            datos.total_servidores,
            datos.total_bases_datos,
            datos.total_sistemas_operativos,
            datos.total_gestores
        ],
        backgroundColor: ['#2563eb', '#10b981', '#f59e0b', '#ef4444']
    }]
}
,
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


const cargarDatosKPIs = async () => {
    try {
        const response = await fetch("/api/kpis", {
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("token")
            }
        });
        if (!response.ok) throw new Error("Error en la respuesta de la API");
        
        const datos = await response.json();
        actualizarKPIsUI(datos);
    } catch (error) {
        console.error("Error cargando datos de KPIs:", error);
    }
};


const actualizarKPIsUI = (datos) => {
    console.log("Datos de KPIs recibidos:", datos);

    // Ejemplo: actualiza tarjetas
    const tarjetas = document.querySelectorAll(".kpi-card .kpi-value");

    if (tarjetas.length >= 4) {
        tarjetas[0].textContent = datos.total_servidores;         // Total servidores
        tarjetas[1].textContent = datos.servidores_activos;       // Servidores activos
        tarjetas[2].textContent = datos.servidores_inactivos;     // Servidores inactivos
        tarjetas[3].textContent = datos.total_bases_datos;        // Bases de datos
        
        print("carga de tarjetas")
        
    }
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