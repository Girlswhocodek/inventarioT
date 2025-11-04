// static/js/sistemas-operativos.js
class SistemasOperativosManager {
    constructor() {
        this.sistemasOperativos = [];
        this.sistemasOperativosFiltrados = [];
        this.filtros = {
            search: '',
            estado: '',
            distribucion: '',
            arquitectura: ''
        };
        this.init();
    }

    async init() {
        await this.cargarEstadisticas();
        await this.cargarSistemasOperativos();
        this.renderizarSistemasOperativos();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Búsqueda con Enter
        document.getElementById('searchInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.buscarSistemasOperativos();
            }
        });

        // Búsqueda en tiempo real con debounce
        let searchTimeout;
        document.getElementById('searchInput').addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.filtros.search = e.target.value;
                this.aplicarFiltros();
            }, 300);
        });
    }

    async cargarEstadisticas() {
        try {
            const response = await this.fetchWithAuth('/api/sistemas-operativos/estadisticas/resumen');
            if (response.ok) {
                const stats = await response.json();
                this.renderizarEstadisticas(stats);
            }
        } catch (error) {
            console.error('Error cargando estadísticas:', error);
        }
    }

    renderizarEstadisticas(stats) {
        const grid = document.getElementById('statsGrid');
        if (!grid) return;

        grid.innerHTML = `
            <div class="kpi-card">
                <div class="kpi-icon icon-system">
                    <i class="fab fa-windows"></i>
                </div>
                <div class="kpi-value">${stats.total_sistemas || 0}</div>
                <div class="kpi-title">Total Sistemas</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon icon-active">
                    <i class="fas fa-check-circle"></i>
                </div>
                <div class="kpi-value">${stats.sistemas_activos || 0}</div>
                <div class="kpi-title">Activos</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon" style="background: linear-gradient(45deg, #ff6b6b, #ee5a24);">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <div class="kpi-value">${stats.sistemas_vencidos || 0}</div>
                <div class="kpi-title">Soporte Vencido</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon" style="background: linear-gradient(45deg, #4834d4, #686de0);">
                    <i class="fas fa-server"></i>
                </div>
                <div class="kpi-value">${stats.servidores_unicos || 0}</div>
                <div class="kpi-title">Servidores</div>
            </div>
        `;
    }

    async cargarSistemasOperativos() {
        try {
            const response = await this.fetchWithAuth('/api/sistemas-operativos');
            if (response.ok) {
                this.sistemasOperativos = await response.json();
                this.sistemasOperativosFiltrados = [...this.sistemasOperativos];
            } else {
                console.error('Error al cargar sistemas operativos');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    buscarSistemasOperativos() {
        const searchInput = document.getElementById('searchInput');
        this.filtros.search = searchInput.value;
        this.aplicarFiltros();
    }

    aplicarFiltros() {
        let resultados = [...this.sistemasOperativos];

        // Filtro de búsqueda
        if (this.filtros.search) {
            const searchTerm = this.filtros.search.toLowerCase();
            resultados = resultados.filter(so => 
                (so.nombre && so.nombre.toLowerCase().includes(searchTerm)) ||
                (so.distribucion && so.distribucion.toLowerCase().includes(searchTerm)) ||
                (so.version && so.version.toLowerCase().includes(searchTerm)) ||
                (so.tipo_usuario && so.tipo_usuario.toLowerCase().includes(searchTerm)) ||
                (so.servidor && so.servidor.nombre && so.servidor.nombre.toLowerCase().includes(searchTerm)) ||
                (so.id && so.id.toString().includes(searchTerm))
            );
        }

        // Filtro por estado
        if (this.filtros.estado) {
            resultados = resultados.filter(so => {
                const estadoSO = so.estado ? so.estado.toLowerCase() : '';
                return estadoSO === this.filtros.estado.toLowerCase();
            });
        }

        // Filtro por distribución
        if (this.filtros.distribucion) {
            resultados = resultados.filter(so => 
                so.distribucion && so.distribucion === this.filtros.distribucion
            );
        }

        // Filtro por arquitectura
        if (this.filtros.arquitectura) {
            resultados = resultados.filter(so => 
                so.arquitectura && so.arquitectura === this.filtros.arquitectura
            );
        }

        this.sistemasOperativosFiltrados = resultados;
        this.renderizarSistemasOperativos();
        this.mostrarNotificacionFiltros();
    }

    mostrarNotificacionFiltros() {
        const total = this.sistemasOperativos.length;
        const filtrados = this.sistemasOperativosFiltrados.length;
        
        if (filtrados !== total) {
            console.log(`Mostrando ${filtrados} de ${total} sistemas operativos`);
        }
    }

    limpiarFiltros() {
        this.filtros = {
            search: '',
            estado: '',
            distribucion: '',
            arquitectura: ''
        };
        
        document.getElementById('searchInput').value = '';
        document.getElementById('filterEstado').value = '';
        document.getElementById('filterDistribucion').value = '';
        document.getElementById('filterArquitectura').value = '';
        
        this.sistemasOperativosFiltrados = [...this.sistemasOperativos];
        this.renderizarSistemasOperativos();
        
        this.mostrarNotificacion('Filtros limpiados correctamente', 'success');
    }

    mostrarNotificacion(mensaje, tipo = 'success') {
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

    renderizarSistemasOperativos() {
        const grid = document.getElementById('sistemasOperativosGrid');
        if (!grid) {
            console.error('Elemento sistemasOperativosGrid no encontrado');
            return;
        }

        if (this.sistemasOperativosFiltrados.length === 0) {
            grid.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">
                        <i class="fab fa-windows"></i>
                    </div>
                    <h3>No se encontraron sistemas operativos</h3>
                    <p>Intenta ajustar los términos de búsqueda o los filtros aplicados</p>
                    ${this.filtros.search || this.filtros.estado || this.filtros.distribucion || this.filtros.arquitectura ? 
                        '<button class="btn-clear-filters" onclick="sistemasOperativosManager.limpiarFiltros()" style="margin-top: 15px;"><i class="fas fa-times"></i> Limpiar todos los filtros</button>' : 
                        ''
                    }
                </div>
            `;
            return;
        }

        grid.innerHTML = this.sistemasOperativosFiltrados.map(so => `
            <div class="server-card" onclick="sistemasOperativosManager.mostrarDetalles(${so.id})">
                <div class="server-header">
                    <div class="server-icon">
                        ${this.getIconoDistribucion(so.distribucion)}
                    </div>
                    <div class="server-status ${this.getStatusClass(so.estado, so.fecha_vencimiento)}">
                        <i class="fas fa-circle"></i>
                    </div>
                </div>
                <div class="server-info">
                    <h3>${this.resaltarBusqueda(so.nombre) || 'Sin nombre'}</h3>
                    <p class="server-distribucion">${so.distribucion || 'Distribución no especificada'} ${so.version || ''}</p>
                    <div class="server-stats">
                        <div class="stat">
                            <span class="stat-label">Arquitectura</span>
                            <span class="stat-value">${so.arquitectura || 'N/A'}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Usuario</span>
                            <span class="stat-value">${so.tipo_usuario || 'N/A'}</span>
                        </div>
                    </div>
                </div>
                <div class="server-footer">
                    <span class="server-servidor">${so.servidor ? so.servidor.nombre : 'Sin servidor'}</span>
                    <span class="server-id">ID: ${so.id}</span>
                </div>
                <div class="status-badge ${this.getStatusClass(so.estado, so.fecha_vencimiento)}">
                    ${this.getEstadoTexto(so.estado, so.fecha_vencimiento)}
                </div>
                ${this.getBadgeSoporte(so.fecha_vencimiento)}
            </div>
        `).join('');
    }

    getIconoDistribucion(distribucion) {
        if (!distribucion) return '<i class="fab fa-linux"></i>';
        
        const distLower = distribucion.toLowerCase();
        if (distLower.includes('windows')) return '<i class="fab fa-windows"></i>';
        if (distLower.includes('linux')) return '<i class="fab fa-linux"></i>';
        if (distLower.includes('ubuntu')) return '<i class="fab fa-ubuntu"></i>';
        if (distLower.includes('redhat') || distLower.includes('rhel')) return '<i class="fab fa-redhat"></i>';
        return '<i class="fab fa-linux"></i>';
    }

    getStatusClass(estado, fechaVencimiento) {
        if (!estado) return 'inactive';
        
        const estadoLower = estado.toLowerCase();
        const hoy = new Date();
        const vencimiento = fechaVencimiento ? new Date(fechaVencimiento) : null;
        
        // Si el soporte está vencido, mostrar como crítico
        if (vencimiento && vencimiento < hoy) {
            return 'critical';
        }
        
        if (estadoLower === 'activo') return 'active';
        if (estadoLower === 'inactivo') return 'inactive';
        if (estadoLower.includes('mantenimiento')) return 'maintenance';
        return 'inactive';
    }

    getEstadoTexto(estado, fechaVencimiento) {
        if (!estado) return 'Inactivo';
        
        const hoy = new Date();
        const vencimiento = fechaVencimiento ? new Date(fechaVencimiento) : null;
        
        if (vencimiento && vencimiento < hoy) {
            return 'Soporte Vencido';
        }
        
        const estadoLower = estado.toLowerCase();
        if (estadoLower === 'activo') return 'Activo';
        if (estadoLower === 'inactivo') return 'Inactivo';
        if (estadoLower.includes('mantenimiento')) return 'Mantenimiento';
        return estado;
    }

    getBadgeSoporte(fechaVencimiento) {
        if (!fechaVencimiento) return '';
        
        const hoy = new Date();
        const vencimiento = new Date(fechaVencimiento);
        const diasRestantes = Math.ceil((vencimiento - hoy) / (1000 * 60 * 60 * 24));
        
        if (diasRestantes < 0) {
            return '<div class="badge badge-danger" style="position: absolute; top: 10px; left: 10px;">Soporte Vencido</div>';
        } else if (diasRestantes <= 30) {
            return `<div class="badge badge-warning" style="position: absolute; top: 10px; left: 10px;">Vence en ${diasRestantes}d</div>`;
        }
        
        return '';
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

    async mostrarDetalles(soId) {
        try {
            const response = await this.fetchWithAuth(`/api/sistemas-operativos/${soId}`);
            if (response.ok) {
                const sistemaOperativo = await response.json();
                this.mostrarModal(sistemaOperativo);
            }
        } catch (error) {
            console.error('Error al cargar detalles:', error);
        }
    }

    mostrarModal(sistemaOperativo) {
        const modal = document.getElementById('sistemaOperativoModal');
        const modalTitle = document.getElementById('modalTitle');
        
        if (!modal || !modalTitle) {
            console.error('Modal elements not found');
            return;
        }
        
        modalTitle.textContent = `Detalles: ${sistemaOperativo.nombre}`;
        this.llenarInformacionGeneral(sistemaOperativo);
        this.llenarLicencias(sistemaOperativo);
        this.llenarPermisos(sistemaOperativo);
        this.llenarServidor(sistemaOperativo);
        
        modal.style.display = 'block';
    }

    llenarInformacionGeneral(so) {
        const container = document.getElementById('sistemaOperativoDetails');
        if (!container) return;
        
        container.innerHTML = `
            <div class="detail-item">
                <label>Nombre:</label>
                <span>${so.nombre || 'N/A'}</span>
            </div>
            <div class="detail-item">
                <label>Distribución:</label>
                <span>${so.distribucion || 'N/A'}</span>
            </div>
            <div class="detail-item">
                <label>Versión:</label>
                <span>${so.version || 'N/A'}</span>
            </div>
            <div class="detail-item">
                <label>Arquitectura:</label>
                <span>${so.arquitectura || 'N/A'}</span>
            </div>
            <div class="detail-item">
                <label>Tipo de Usuario:</label>
                <span>${so.tipo_usuario || 'N/A'}</span>
            </div>
            <div class="detail-item">
                <label>Estado:</label>
                <span class="status ${this.getStatusClass(so.estado, so.fecha_vencimiento)}">
                    ${this.getEstadoTexto(so.estado, so.fecha_vencimiento)}
                </span>
            </div>
            <div class="detail-item">
                <label>Fecha Creación:</label>
                <span>${so.fecha_creacion ? new Date(so.fecha_creacion).toLocaleDateString() : 'N/A'}</span>
            </div>
            <div class="detail-item">
                <label>Última Actualización:</label>
                <span>${so.fecha_actualizacion ? new Date(so.fecha_actualizacion).toLocaleString() : 'N/A'}</span>
            </div>
        `;
    }

    llenarLicencias(so) {
        const container = document.getElementById('licenciasContent');
        if (!container) return;
        
        const hoy = new Date();
        const vencimiento = so.fecha_vencimiento ? new Date(so.fecha_vencimiento) : null;
        const diasRestantes = vencimiento ? Math.ceil((vencimiento - hoy) / (1000 * 60 * 60 * 24)) : null;
        
        container.innerHTML = `
            <div class="detail-grid">
                <div class="detail-item">
                    <label>Licencia:</label>
                    <span>${so.licencia || 'No especificada'}</span>
                </div>
                <div class="detail-item">
                    <label>Fecha Vencimiento Soporte:</label>
                    <span class="${vencimiento && vencimiento < hoy ? 'status critical' : 'status active'}">
                        ${so.fecha_vencimiento ? new Date(so.fecha_vencimiento).toLocaleDateString() : 'No especificada'}
                        ${diasRestantes !== null ? ` (${diasRestantes > 0 ? `${diasRestantes} días restantes` : 'Vencido'})` : ''}
                    </span>
                </div>
                <div class="detail-item">
                    <label>Estado Soporte:</label>
                    <span class="${vencimiento && vencimiento < hoy ? 'badge badge-danger' : 'badge badge-success'}">
                        ${vencimiento && vencimiento < hoy ? 'SOPORTE VENCIDO' : 'SOPORTE VIGENTE'}
                    </span>
                </div>
            </div>
            ${vencimiento && vencimiento < hoy ? `
                <div class="alert alert-warning" style="margin-top: 20px; padding: 15px; background: #fff3cd; border-radius: 8px; border-left: 4px solid #ffc107;">
                    <strong>⚠️ Advertencia:</strong> El soporte para esta versión ha vencido. Considere actualizar el sistema operativo.
                </div>
            ` : ''}
        `;
    }

    llenarPermisos(so) {
        const container = document.getElementById('permisosContent');
        if (!container) return;
        
        const permisos = so.permisos || {};
        const usuarios = permisos.usuarios || [];
        const grupos = permisos.grupos || [];
        
        container.innerHTML = `
            <div class="detail-grid">
                <div class="detail-item">
                    <label>Usuarios con Acceso:</label>
                    <span>${usuarios.length > 0 ? usuarios.join(', ') : 'No especificados'}</span>
                </div>
                <div class="detail-item">
                    <label>Grupos de Usuarios:</label>
                    <span>${grupos.length > 0 ? grupos.join(', ') : 'No especificados'}</span>
                </div>
            </div>
            
            ${usuarios.length > 0 || grupos.length > 0 ? `
                <div style="margin-top: 20px;">
                    <h4>Resumen de Permisos</h4>
                    <div class="table-container">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Tipo</th>
                                    <th>Nombre</th>
                                    <th>Cantidad</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${usuarios.length > 0 ? `
                                    <tr>
                                        <td>Usuarios</td>
                                        <td>${usuarios.join(', ')}</td>
                                        <td>${usuarios.length}</td>
                                    </tr>
                                ` : ''}
                                ${grupos.length > 0 ? `
                                    <tr>
                                        <td>Grupos</td>
                                        <td>${grupos.join(', ')}</td>
                                        <td>${grupos.length}</td>
                                    </tr>
                                ` : ''}
                            </tbody>
                        </table>
                    </div>
                </div>
            ` : `
                <div class="empty-state">
                    <div class="empty-icon">
                        <i class="fas fa-user-lock"></i>
                    </div>
                    <p>No hay información de permisos configurada</p>
                </div>
            `}
        `;
    }

    llenarServidor(so) {
        const container = document.getElementById('servidorContent');
        if (!container) return;
        
        const servidor = so.servidor;
        
        if (servidor) {
            container.innerHTML = `
                <div class="detail-grid">
                    <div class="detail-item">
                        <label>Nombre del Servidor:</label>
                        <span>${servidor.nombre || 'N/A'}</span>
                    </div>
                    <div class="detail-item">
                        <label>IP:</label>
                        <span>${servidor.ip || 'N/A'}</span>
                    </div>
                    <div class="detail-item">
                        <label>Ambiente:</label>
                        <span>${servidor.ambiente || 'N/A'}</span>
                    </div>
                    <div class="detail-item">
                        <label>Ubicación:</label>
                        <span>${servidor.ubicacion || 'N/A'}</span>
                    </div>
                    <div class="detail-item">
                        <label>Estado:</label>
                        <span class="status ${servidor.estado === 'activo' ? 'active' : 'inactive'}">
                            ${servidor.estado || 'N/A'}
                        </span>
                    </div>
                </div>
                <div style="margin-top: 20px;">
                    <button class="btn-edit" onclick="window.location.href='/servidores?id=${servidor.id}'">
                        <i class="fas fa-external-link-alt"></i> Ver Detalles del Servidor
                    </button>
                </div>
            `;
        } else {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">
                        <i class="fas fa-server"></i>
                    </div>
                    <p>No hay servidor asociado a este sistema operativo</p>
                </div>
            `;
        }
    }

    fetchWithAuth(url, options = {}) {
        const token = localStorage.getItem('access_token');
        options.headers = {
            ...options.headers,
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };
        return fetch(url, options);
    }
}

// Funciones globales para el modal
function closeModal() {
    const modal = document.getElementById('sistemaOperativoModal');
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
    alert('Modo edición - Por implementar');
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    window.sistemasOperativosManager = new SistemasOperativosManager();
});

window.onclick = function(event) {
    const modal = document.getElementById('sistemaOperativoModal');
    if (event.target == modal) {
        closeModal();
    }
}