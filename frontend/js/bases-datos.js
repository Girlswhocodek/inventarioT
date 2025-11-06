// static/js/bases-datos.js
class BasesDatosManager {
    constructor() {
        this.basesDatos = [];
        this.init();
    }

    async init() {
        await this.cargarEstadisticas();
        await this.cargarBasesDatos();
        this.renderizarBasesDatos();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Si agregas un search input en el futuro
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.buscarBasesDatos();
                }
            });
        }
    }

    async cargarEstadisticas() {
        try {
            const response = await this.fetchWithAuth('/api/bases-datos/estadisticas/resumen');
            if (response.ok) {
                const stats = await response.json();
                this.renderizarEstadisticas(stats);
            }
        } catch (error) {
            console.error('Error cargando estadísticas:', error);
        }
    }
    aplicarFiltros() {
        let resultados = [...this.basesDatos];

        // Filtro de búsqueda
        if (this.filtros.search) {
            const searchTerm = this.filtros.search.toLowerCase();
            resultados = resultados.filter(bd => 
                (bd.nombre && bd.nombre.toLowerCase().includes(searchTerm)) ||
                (bd.motor && bd.motor.toLowerCase().includes(searchTerm)) ||
                (bd.responsable && bd.responsable.toLowerCase().includes(searchTerm)) ||
                (bd.id && bd.id.toString().includes(searchTerm)) ||
                (bd.version && bd.version.toLowerCase().includes(searchTerm)) ||
                (bd.instancia && bd.instancia.toLowerCase().includes(searchTerm))
            );
        }

        // Filtro por estado
        if (this.filtros.estado) {
            resultados = resultados.filter(bd => {
                const estadoBD = bd.estado ? bd.estado.toLowerCase() : '';
                return estadoBD === this.filtros.estado.toLowerCase();
            });
        }

        // Filtro por motor
        if (this.filtros.motor) {
            resultados = resultados.filter(bd => 
                bd.motor && bd.motor === this.filtros.motor
            );
        }

        this.basesDatosFiltradas = resultados;
        this.renderizarBasesDatos();
        this.mostrarNotificacionFiltros();
    }

    mostrarNotificacionFiltros() {
        const total = this.basesDatos.length;
        const filtrados = this.basesDatosFiltradas.length;
        
        // Puedes agregar una notificación sutil aquí si lo deseas
        if (filtrados !== total) {
            console.log(`Mostrando ${filtrados} de ${total} bases de datos`);
        }
    }

    limpiarFiltros() {
        this.filtros = {
            search: '',
            estado: '',
            motor: ''
        };
        
        document.getElementById('searchInput').value = '';
        document.getElementById('filterEstado').value = '';
        document.getElementById('filterMotor').value = '';
        
        this.basesDatosFiltradas = [...this.basesDatos];
        this.renderizarBasesDatos();
        
        // Mostrar notificación de éxito
        this.mostrarNotificacion('Filtros limpiados correctamente', 'success');
    }

    mostrarNotificacion(mensaje, tipo = 'success') {
        // Crear notificación temporal
        const notification = document.createElement('div');
        notification.className = `notification ${tipo}`;
        notification.textContent = mensaje;
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.padding = '12px 20px';
        notification.style.borderRadius = '8px';
        notification.style.color = 'white';
        notification.style.fontWeight = 'bold';
        notification.style.zIndex = '1000';
        notification.style.animation = 'slideIn 0.3s ease';
        notification.style.backgroundColor = tipo === 'success' ? '#28a745' : '#dc3545';
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
resaltarBusqueda(texto) {
        if (!this.filtros.search || !texto) return texto;
        
        const searchTerm = this.filtros.search.toLowerCase();
        const textoLower = texto.toLowerCase();
        
        if (textoLower.includes(searchTerm)) {
            const index = textoLower.indexOf(searchTerm);
            const before = texto.substring(0, index);
            const match = texto.substring(index, index + searchTerm.length);
            const after = texto.substring(index + searchTerm.length);
            
            return `${before}<span class="search-highlight">${match}</span>${after}`;
        }
        
        return texto;
    }

    getStatusClass(estado) {
        if (!estado) return 'offline';
        
        const estadoLower = estado.toLowerCase();
        if (estadoLower === 'online') return 'online';
        if (estadoLower === 'offline') return 'offline';
        if (estadoLower.includes('mantenimiento')) return 'maintenance';
        return 'offline';
    }

    getEstadoTexto(estado) {
        if (!estado) return 'Offline';
        
        const estadoLower = estado.toLowerCase();
        if (estadoLower === 'online') return 'En Línea';
        if (estadoLower === 'offline') return 'Offline';
        if (estadoLower.includes('mantenimiento')) return 'Mantenimiento';
        return estado;
    }

    renderizarEstadisticas(stats) {
        // Si decides agregar estadísticas, necesitarás este elemento en el HTML
        const grid = document.getElementById('statsGrid');
        if (!grid) return;

        grid.innerHTML = `
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-database"></i>
                </div>
                <div class="stat-info">
                    <h3>${stats.total_bases_datos || 0}</h3>
                    <p>Total Bases</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon online">
                    <i class="fas fa-check-circle"></i>
                </div>
                <div class="stat-info">
                    <h3>${stats.bases_online || 0}</h3>
                    <p>En Línea</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon warning">
                    <i class="fas fa-exclamation-circle"></i>
                </div>
                <div class="stat-info">
                    <h3>${stats.bases_offline || 0}</h3>
                    <p>Offline</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-hdd"></i>
                </div>
                <div class="stat-info">
                    <h3>${stats.espacio_total_gb ? stats.espacio_total_gb.toFixed(1) : '0'}</h3>
                    <p>Espacio Total (GB)</p>
                </div>
            </div>
        `;
    }

    async cargarBasesDatos() {
        try {
            const response = await this.fetchWithAuth('/api/bases-datos');
            if (response.ok) {
                this.basesDatos = await response.json();
            } else {
                console.error('Error al cargar bases de datos');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    renderizarBasesDatos() {
        const grid = document.getElementById('databasesGrid'); // Cambiado de 'basesDatosGrid'
        if (!grid) {
            console.error('Elemento databasesGrid no encontrado');
            return;
        }

        if (this.basesDatos.length === 0) {
            grid.innerHTML = `
                <div class="no-data">
                    <i class="fas fa-database"></i>
                    <p>No hay bases de datos registradas</p>
                </div>
            `;
            return;
        }

        grid.innerHTML = this.basesDatos.map(bd => `
            <div class="server-card" onclick="basesDatosManager.mostrarDetalles(${bd.id})">
                <div class="server-header">
                    <div class="server-icon">
                        <i class="fas fa-database"></i>
                    </div>
                    <div class="server-status ${bd.estado?.toLowerCase() === 'online' ? 'active' : 'inactive'}">
                        <i class="fas fa-circle"></i>
                    </div>
                </div>
                <div class="server-info">
                    <h3>${bd.nombre || 'Sin nombre'}</h3>
                    <p>${bd.motor || 'Motor no especificado'} ${bd.version || ''}</p>
                    <div class="server-stats">
                        <div class="stat">
                            <span class="stat-label">Espacio</span>
                            <span class="stat-value">${bd.espacio_total_gb ? bd.espacio_total_gb.toFixed(1) : '0'} GB</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Objetos</span>
                            <span class="stat-value">${bd.objetos || 0}</span>
                        </div>
                    </div>
                </div>
                <div class="server-footer">
                    <span class="server-responsable">${bd.responsable || 'No asignado'}</span>
                </div>
            </div>
        `).join('');
    }

    async buscarBasesDatos() {
        const searchInput = document.getElementById('searchInput');
        if (!searchInput) return;
        
        const query = searchInput.value;
        if (!query.trim()) {
            this.renderizarBasesDatos();
            return;
        }

        try {
            const response = await this.fetchWithAuth(`/buscar?q=${encodeURIComponent(query)}&nivel=bases_datos`);
            if (response.ok) {
                const data = await response.json();
                this.mostrarResultadosBusqueda(data.bases_datos || []);
            }
        } catch (error) {
            console.error('Error en búsqueda:', error);
        }
    }

    mostrarResultadosBusqueda(resultados) {
        const grid = document.getElementById('databasesGrid'); // Cambiado de 'basesDatosGrid'
        if (!grid) return;

        if (resultados.length === 0) {
            grid.innerHTML = `
                <div class="no-data">
                    <i class="fas fa-search"></i>
                    <p>No se encontraron bases de datos</p>
                </div>
            `;
            return;
        }

        grid.innerHTML = resultados.map(bd => `
            <div class="server-card" onclick="basesDatosManager.mostrarDetalles(${bd.id})">
                <div class="server-header">
                    <div class="server-icon">
                        <i class="fas fa-database"></i>
                    </div>
                    <div class="server-status ${bd.estado?.toLowerCase() === 'online' ? 'active' : 'inactive'}">
                        <i class="fas fa-circle"></i>
                    </div>
                </div>
                <div class="server-info">
                    <h3>${bd.nombre || 'Sin nombre'}</h3>
                    <p>${bd.motor || 'Motor no especificado'} ${bd.version || ''}</p>
                    <div class="server-stats">
                        <div class="stat">
                            <span class="stat-label">Espacio</span>
                            <span class="stat-value">${bd.espacio_total_gb ? bd.espacio_total_gb.toFixed(1) : '0'} GB</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Objetos</span>
                            <span class="stat-value">${bd.objetos || 0}</span>
                        </div>
                    </div>
                </div>
                <div class="server-footer">
                    <span class="server-responsable">${bd.responsable || 'No asignado'}</span>
                </div>
            </div>
        `).join('');
    }

    async mostrarDetalles(bdId) {
        try {
            const response = await this.fetchWithAuth(`/api/bases-datos/${bdId}`);
            if (response.ok) {
                const baseDatos = await response.json();
                this.mostrarModal(baseDatos);
            }
        } catch (error) {
            console.error('Error al cargar detalles:', error);
        }
    }

    mostrarModal(baseDatos) {
        const modal = document.getElementById('databaseModal'); // Cambiado de 'baseDatosModal'
        const modalTitle = document.getElementById('modalTitle');
        
        if (!modal || !modalTitle) {
            console.error('Modal elements not found');
            return;
        }
        
        modalTitle.textContent = `Detalles: ${baseDatos.nombre}`;
        this.llenarInformacionGeneral(baseDatos);
        this.llenarObjetos(baseDatos);
        this.llenarResponsable(baseDatos);
        this.llenarConfiguracion(baseDatos);
        this.llenarMonitoreo(baseDatos);
        
        modal.style.display = 'block';
    }

    llenarInformacionGeneral(bd) {
        const container = document.getElementById('databaseDetails'); // Cambiado de 'baseDatosDetails'
        if (!container) return;
        
        container.innerHTML = `
            <div class="detail-item">
                <label>Nombre:</label>
                <span>${bd.nombre || 'N/A'}</span>
            </div>
            <div class="detail-item">
                <label>Motor:</label>
                <span>${bd.motor || 'N/A'}</span>
            </div>
            <div class="detail-item">
                <label>Versión:</label>
                <span>${bd.version || 'N/A'}</span>
            </div>
            <div class="detail-item">
                <label>Estado:</label>
                <span class="status ${bd.estado?.toLowerCase() === 'online' ? 'active' : 'inactive'}">${bd.estado || 'N/A'}</span>
            </div>
            <div class="detail-item">
                <label>Puerto:</label>
                <span>${bd.puerto || 'N/A'}</span>
            </div>
            <div class="detail-item">
                <label>Fecha Inicio:</label>
                <span>${bd.fecha_inicio ? new Date(bd.fecha_inicio).toLocaleDateString() : 'N/A'}</span>
            </div>
            <div class="detail-item">
                <label>URL Conexión:</label>
                <span>${bd.url_conexion || 'N/A'}</span>
            </div>
        `;
    }

    llenarObjetos(bd) {
        const container = document.getElementById('objetosContent');
        if (!container) return;
        
        const objetos = bd.objetos_bd || [];
        
        if (objetos.length > 0) {
            container.innerHTML = `
                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Nombre</th>
                                <th>Tipo</th>
                                <th>Tamaño (MB)</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${objetos.map(obj => `
                                <tr>
                                    <td>${obj.nombre}</td>
                                    <td>${obj.tipo}</td>
                                    <td>${obj.tamaño_mb ? obj.tamaño_mb.toFixed(2) : '0'}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
                <div class="summary">
                    <p><strong>Total objetos:</strong> ${objetos.length}</p>
                </div>
            `;
        } else {
            container.innerHTML = '<p class="no-data">No hay objetos registrados para esta base de datos.</p>';
        }
    }

    llenarResponsable(bd) {
        const container = document.getElementById('responsableContent');
        if (!container) return;
        
        const admin = bd.administrador;
        
        if (admin) {
            container.innerHTML = `
                <div class="detail-grid">
                    <div class="detail-item">
                        <label>Nombre:</label>
                        <span>${admin.nombre_completo}</span>
                    </div>
                    <div class="detail-item">
                        <label>Email:</label>
                        <span>${admin.email}</span>
                    </div>
                    <div class="detail-item">
                        <label>Cargo:</label>
                        <span>${admin.cargo}</span>
                    </div>
                </div>
            `;
        } else {
            container.innerHTML = '<p class="no-data">No hay administrador asignado.</p>';
        }
    }

    llenarConfiguracion(bd) {
        const container = document.getElementById('configuracionContent');
        if (!container) return;
        
        container.innerHTML = `
            <div class="detail-grid">
                <div class="detail-item">
                    <label>Character Set:</label>
                    <span>${bd.caracter_set || 'N/A'}</span>
                </div>
                <div class="detail-item">
                    <label>NLS Character Set:</label>
                    <span>${bd.nls_characterset || 'N/A'}</span>
                </div>
                <div class="detail-item">
                    <label>Espacio Total:</label>
                    <span>${bd.espacio_total_gb ? bd.espacio_total_gb.toFixed(2) + ' GB' : 'N/A'}</span>
                </div>
                <div class="detail-item">
                    <label>Espacio Objetos:</label>
                    <span>${bd.espacio_objetos_gb ? bd.espacio_objetos_gb.toFixed(2) + ' GB' : 'N/A'}</span>
                </div>
                <div class="detail-item">
                    <label>DB Links:</label>
                    <span>${bd.dblinks ? (Array.isArray(bd.dblinks) ? bd.dblinks.join(', ') : bd.dblinks) : 'Ninguno'}</span>
                </div>
            </div>
        `;
    }

    llenarMonitoreo(bd) {
        const container = document.getElementById('monitoreoContent');
        if (!container) return;
        
        container.innerHTML = `
            <div class="detail-grid">
                <div class="detail-item">
                    <label>Estado Actual:</label>
                    <span class="status ${bd.esta_online ? 'active' : 'inactive'}">
                        ${bd.esta_online ? 'EN LÍNEA' : 'FUERA DE LÍNEA'}
                    </span>
                </div>
                <div class="detail-item">
                    <label>Porcentaje Uso Espacio:</label>
                    <span>${bd.porcentaje_uso_espacio ? bd.porcentaje_uso_espacio.toFixed(2) + '%' : 'N/A'}</span>
                </div>
                <div class="detail-item">
                    <label>Última Actualización:</label>
                    <span>${bd.fecha_actualizacion ? new Date(bd.fecha_actualizacion).toLocaleString() : 'N/A'}</span>
                </div>
                <div class="detail-item">
                    <label>Fecha Creación:</label>
                    <span>${bd.fecha_creacion ? new Date(bd.fecha_creacion).toLocaleDateString() : 'N/A'}</span>
                </div>
            </div>
        `;
    }

    fetchWithAuth(url, options = {}) {
        const token = localStorage.getItem('access_token');
        options.headers = {
            ...options.headers,
            'Authorization': `Bearer ${token}`
        };
        return fetch(url, options);
    }
}

// Funciones globales para el modal
function closeModal() {
    const modal = document.getElementById('databaseModal'); // Cambiado de 'baseDatosModal'
    if (modal) {
        modal.style.display = 'none';
    }
}

function openTab(evt, tabName) {
    const tabcontent = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("active");
    }

    const tabbuttons = document.getElementsByClassName("tab-button");
    for (let i = 0; i < tabbuttons.length; i++) {
        tabbuttons[i].classList.remove("active");
    }

    const targetTab = document.getElementById(tabName);
    if (targetTab) {
        targetTab.classList.add("active");
    }
    
    if (evt && evt.currentTarget) {
        evt.currentTarget.classList.add("active");
    }
}

function toggleEditMode() {
    // Implementar lógica de edición
    alert('Modo edición - Por implementar');
}


// Manejar clic fuera del modal para cerrarlo
window.onclick = function(event) {
    const modal = document.getElementById('databaseModal'); // Cambiado de 'baseDatosModal'
    if (event.target == modal) {
        closeModal();
    }
}