// Cargar servidores al inicio
        function loadServers() {
            const grid = document.getElementById('serversGrid');
            grid.innerHTML = '';

            servidoresData.forEach(servidor => {
                const card = createServerCard(servidor);
                grid.appendChild(card);
            });
        }

        // Crear tarjeta de servidor
        function createServerCard(servidor) {
            const card = document.createElement('div');
            card.className = 'server-card';
            card.dataset.id = servidor.id;
            card.onclick = () => openServerModal(servidor);
            
            card.innerHTML = `
                <div class="server-header">
                    <div class="server-name">${servidor.nombre}</div>
                    <div class="server-ip">${servidor.ip || 'Sin IP'}</div>
                    <div class="server-status status-${servidor.estado}">
                        ${servidor.estado.toUpperCase()}
                    </div>
                </div>
                <div class="server-info">
                    <div class="server-specs">
                        <div class="spec-item">
                            <div class="spec-label">CPU</div>
                            <div class="spec-value">${servidor.cpu_nucleos || 'N/A'} cores</div>
                        </div>
                        <div class="spec-item">
                            <div class="spec-label">RAM</div>
                            <div class="spec-value">${servidor.ram_gb || 'N/A'} GB</div>
                        </div>
                        <div class="spec-item">
                            <div class="spec-label">Tecnología</div>
                            <div class="spec-value">${servidor.tecnologia || 'N/A'}</div>
                        </div>
                        <div class="spec-item">
                            <div class="spec-label">Fabricante</div>
                            <div class="spec-value">${servidor.fabricante || 'N/A'}</div>
                        </div>
                    </div>
                </div>
            `;
            
            return card;
        }

        // Abrir modal del servidor
        function openServerModal(servidor) {
            document.getElementById('modalTitle').textContent = `${servidor.nombre} - Gestión Completa`;
            document.getElementById('serverModal').style.display = 'block';
            
            // Cargar información general
            loadGeneralInfo(servidor);
            
            // Resetear a la primera pestaña
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            document.querySelector('.tab-button').classList.add('active');
            document.getElementById('info-general').classList.add('active');
            
            // Guardar servidor actual para usar en otras pestañas
            window.currentServer = servidor;
        }

        // Cargar información general
        function loadGeneralInfo(servidor) {
            const container = document.getElementById('serverDetails');
            container.innerHTML = `
                <div class="detail-card">
                    <div class="detail-label">Nombre del Servidor</div>
                    <div class="detail-value">${servidor.nombre}</div>
                </div>
                <div class="detail-card" data-field="ip">
                    <div class="detail-label">Dirección IP</div>
                    <div class="detail-value">${servidor.ip || 'N/A'}</div>
                </div>
                <div class="detail-card" data-field="estado">
                    <div class="detail-label">Estado</div>
                    <div class="detail-value">
                        <span class="badge badge-${servidor.estado === 'activo' ? 'success' : 'danger'}">
                            ${servidor.estado.toUpperCase()}
                        </span>
                    </div>
                </div>
                <div class="detail-card" data-field="tecnología">
                    <div class="detail-label">Tecnología</div>
                    <div class="detail-value">${servidor.tecnologia || 'N/A'}</div>
                </div>
                <div class="detail-card" data-field="nucleos">
                    <div class="detail-label">CPU (Núcleos)</div>
                    <div class="detail-value">${servidor.cpu_nucleos || 'N/A'}</div>
                </div>
                <div class="detail-card" data-field="ram">
                    <div class="detail-label">RAM (GB)</div>
                    <div class="detail-value">${servidor.ram_gb || 'N/A'} GB</div>
                </div>
                <div class="detail-card" data-field="almacenamiento">
                    <div class="detail-label">Almacenamiento (GB)</div>
                    <div class="detail-value">${servidor.almacenamiento_gb || 'N/A'} GB</div>
                </div>
                <div class="detail-card" data-field="arquitectura">
                    <div class="detail-label">Arquitectura</div>
                    <div class="detail-value">${servidor.arquitectura || 'N/A'}</div>
                </div>
                <div class="detail-card" data-field="fabricante">
                    <div class="detail-label">Fabricante</div>
                    <div class="detail-value">${servidor.fabricante || 'N/A'}</div>
                </div>
                <div class="detail-card" data-field="modelo">
                    <div class="detail-label">Modelo</div>
                    <div class="detail-value">${servidor.modelo || 'N/A'}</div>
                </div>
                <div class="detail-card" data-field="particionado">
                    <div class="detail-label">Particionado</div>
                    <div class="detail-value">
                        <span class="badge badge-${servidor.particionado ? 'success' : 'warning'}">
                            ${servidor.particionado ? 'SÍ' : 'NO'}
                        </span>
                    </div>
                </div>
                <div class="detail-card" data-field="ubicación">
                    <div class="detail-label">Ubicación</div>
                    <div class="detail-value">${servidor.ubicacion || 'N/A'}</div>
                </div>
                <div class="detail-card" data-field="responsable">
                    <div class="detail-label">Responsable</div>
                    <div class="detail-value">${servidor.responsable || 'N/A'}</div>
                </div>
            `;
        }

        // Función para cambiar de pestaña
        function openTab(evt, tabName) {
            // Ocultar todos los contenidos de pestañas
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            // Desactivar todos los botones
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Mostrar el contenido seleccionado y activar el botón
            document.getElementById(tabName).classList.add('active');
            evt.currentTarget.classList.add('active');
            
            // Cargar contenido específico según la pestaña
            loadTabContent(tabName);
        }

        // Cargar contenido específico de cada pestaña
        function loadTabContent(tabName) {
            const serverId = window.currentServer.id;
            
            switch(tabName) {
                case 'sistemas-operativos':
                    loadSistemasOperativos(serverId);
                    break;
                case 'instancias-bd':
                    loadInstanciasBd(serverId);
                    break;
                case 'discos':
                    loadDiscos(serverId);
                    break;
                case 'monitoreo':
                    loadMonitoreo(serverId);
                    break;
            }
        }

        // Cargar sistemas operativos
        function loadSistemasOperativos(serverId) {
            const container = document.getElementById('sistemasContent');
            const sistemas = sistemasOperativos[serverId] || [];
            
            if (sistemas.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-icon">💿</div>
                        <h4>No hay sistemas operativos registrados</h4>
                        <p>Este servidor no tiene sistemas operativos configurados.</p>
                    </div>
                `;
                return;
            }
            
            container.innerHTML = `
                <table class="related-table">
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Versión</th>
                            <th>Tipo</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${sistemas.map(so => `
                            <tr>
                                <td><strong>${so.nombre}</strong></td>
                                <td>${so.version}</td>
                                <td><span class="badge badge-info">${so.tipo}</span></td>
                                <td><span class="badge badge-success">Instalado</span></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        }

        // Cargar instancias de BD
        function loadInstanciasBd(serverId) {
            const container = document.getElementById('instanciasContent');
            const instancias = instanciasBd[serverId] || [];
            
            if (instancias.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-icon">🗄️</div>
                        <h4>No hay bases de datos configuradas</h4>
                        <p>Este servidor no tiene instancias de bases de datos.</p>
                    </div>
                `;
                return;
            }
            
            container.innerHTML = `
                <table class="related-table">
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Motor</th>
                            <th>Versión</th>
                            <th>Puerto</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${instancias.map(bd => `
                            <tr>
                                <td><strong>${bd.nombre}</strong></td>
                                <td>${bd.motor}</td>
                                <td>${bd.version}</td>
                                <td>${bd.puerto}</td>
                                <td><span class="badge badge-${bd.estado === 'activo' ? 'success' : 'danger'}">${bd.estado.toUpperCase()}</span></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        }

        // Cargar discos
        function loadDiscos(serverId) {
            const container = document.getElementById('discosContent');
            const discosData = discos[serverId] || [];
            
            if (discosData.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-icon">💾</div>
                        <h4>No hay discos configurados</h4>
                        <p>Este servidor no tiene información de discos.</p>
                    </div>
                `;
                return;
            }
            
            container.innerHTML = `
                <table class="related-table">
                    <thead>
                        <tr>
                            <th>Dispositivo</th>
                            <th>Tamaño (GB)</th>
                            <th>Tipo</th>
                            <th>Punto de Montaje</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${discosData.map(disco => `
                            <tr>
                                <td><strong>${disco.dispositivo}</strong></td>
                                <td>${disco.tamaño_gb} GB</td>
                                <td><span class="badge badge-info">${disco.tipo}</span></td>
                                <td>${disco.punto_montaje}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        }

        // Cargar información de monitoreo
        function loadMonitoreo(serverId) {
            const container = document.getElementById('monitoreoContent');
            const servidor = window.currentServer;
            
            container.innerHTML = `
                <div class="detail-grid">
                    <div class="detail-card">
                        <div class="detail-label">Estado del Servidor</div>
                        <div class="detail-value">
                            <span class="badge badge-${servidor.estado === 'activo' ? 'success' : 'danger'}">
                                ${servidor.estado === 'activo' ? '🟢 ACTIVO' : '🔴 INACTIVO'}
                            </span>
                        </div>
                    </div>
                    <div class="detail-card">
                        <div class="detail-label">Uso de CPU</div>
                        <div class="detail-value">
                            <span class="badge badge-success">📊 ${Math.floor(Math.random() * 30 + 10)}%</span>
                        </div>
                    </div>
                    <div class="detail-card">
                        <div class="detail-label">Uso de RAM</div>
                        <div class="detail-value">
                            <span class="badge badge-warning">💾 ${Math.floor(Math.random() * 40 + 20)}%</span>
                        </div>
                    </div>
                    <div class="detail-card">
                        <div class="detail-label">Espacio en Disco</div>
                        <div class="detail-value">
                            <span class="badge badge-info">💽 ${Math.floor(Math.random() * 50 + 30)}% usado</span>
                        </div>
                    </div>
                    <div class="detail-card">
                        <div class="detail-label">Conectividad</div>
                        <div class="detail-value">
                            <span class="badge badge-success">🌐 CONECTADO</span>
                        </div>
                    </div>
                    <div class="detail-card">
                        <div class="detail-label">Último Check</div>
                        <div class="detail-value">
                            <span class="badge badge-info">⏰ ${new Date().toLocaleString('es-ES')}</span>
                        </div>
                    </div>
                    <div class="detail-card">
                        <div class="detail-label">Uptime</div>
                        <div class="detail-value">
                            <span class="badge badge-success">⏱️ ${Math.floor(Math.random() * 30 + 1)} días</span>
                        </div>
                    </div>
                    <div class="detail-card">
                        <div class="detail-label">Temperatura</div>
                        <div class="detail-value">
                            <span class="badge badge-warning">🌡️ ${Math.floor(Math.random() * 20 + 40)}°C</span>
                        </div>
                    </div>
                </div>
                
                <h4 style="margin: 30px 0 15px 0;">📈 Gráfico de Rendimiento (Simulado)</h4>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;">
                    <p style="color: #6c757d; font-size: 1.1em;">
                        🚧 Aquí iría un gráfico en tiempo real del rendimiento del servidor
                    </p>
                    <p style="color: #6c757d;">
                        Mostraría: CPU, RAM, Disco, Red, etc.
                    </p>
                </div>
            `;
        }

        // Cerrar modal
        function closeModal() {
            document.getElementById('serverModal').style.display = 'none';
        }

        

        // Cerrar sidebar al hacer clic fuera en móviles
        document.addEventListener('click', function(event) {
            const sidebar = document.getElementById('sidebar');
            const menuBtn = document.querySelector('.mobile-menu-btn');
            
            if (window.innerWidth <= 768 && 
                !sidebar.contains(event.target) && 
                !menuBtn.contains(event.target)) {
                sidebar.classList.remove('active');
            }
        });

        // Cerrar modal al hacer clic fuera
        window.onclick = function(event) {
            const modal = document.getElementById('serverModal');
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        }
        // Cargar servidores al cargar la página
        document.addEventListener('DOMContentLoaded', loadServers);
        
       // --------------------------
// Modo edición mejorado con data-field
let isEditMode = false;

function toggleEditMode() {
    isEditMode = !isEditMode;
    const editBtn = document.querySelector('.btn-edit');
    const detailCards = document.querySelectorAll('.detail-card');
    
    if (isEditMode) {
        // Cambiar a modo "Guardar"
        editBtn.innerHTML = '<i class="fas fa-save"></i> Guardar';
        editBtn.classList.add('btn-save');

        detailCards.forEach(card => {
            const valueElement = card.querySelector('.detail-value');
            const currentValue = valueElement.innerText.trim();
            const fieldName = card.dataset.field;

            // Cambiar contenido a input según el tipo de campo
            if (fieldName === 'estado') {
                valueElement.innerHTML = `
                    <select class="edit-input" data-field="${fieldName}">
                        <option value="activo" ${currentValue.includes('ACTIVO') ? 'selected' : ''}>ACTIVO</option>
                        <option value="inactivo" ${currentValue.includes('INACTIVO') ? 'selected' : ''}>INACTIVO</option>
                        <option value="mantenimiento" ${currentValue.includes('MANTENIMIENTO') ? 'selected' : ''}>MANTENIMIENTO</option>
                    </select>
                `;
            } else if (fieldName === 'particionado') {
                valueElement.innerHTML = `
                    <select class="edit-input" data-field="${fieldName}">
                        <option value="true" ${currentValue.includes('SÍ') ? 'selected' : ''}>SÍ</option>
                        <option value="false" ${currentValue.includes('NO') ? 'selected' : ''}>NO</option>
                    </select>
                `;
            } else {
                valueElement.innerHTML = `
                    <input type="text" class="edit-input" data-field="${fieldName}" 
                           value="${currentValue.replace(' GB','')}" 
                           style="width: 100%; padding: 5px;">
                `;
            }
        });

    } else {
        // Guardar cambios
        saveChanges();

        // Volver a modo "Editar"
        editBtn.innerHTML = '<i class="fas fa-edit"></i> Editar';
        editBtn.classList.remove('btn-save');

        // Recargar la vista normal del servidor
        loadGeneralInfo(window.currentServer);
    }
}

function saveChanges() {
    const inputs = document.querySelectorAll('.edit-input');
    const updatedServer = { ...window.currentServer };

    inputs.forEach(input => {
        const field = input.dataset.field;
        let value = input.value;

        // Conversión de tipos
        if (['cpu_nucleos', 'ram_gb', 'almacenamiento_gb'].includes(field)) {
            value = parseInt(value) || 0;
        } else if (field === 'particionado') {
            value = value === 'true';
        }

        updatedServer[field] = value;
    });

    // Actualizar datos globales
    const index = servidoresData.findIndex(s => s.id === updatedServer.id);
    if (index !== -1) {
        servidoresData[index] = updatedServer;
        window.currentServer = updatedServer;

        // Mostrar mensaje
        showNotification('Cambios guardados exitosamente ✅', 'success');

        // Actualizar la tarjeta del grid
        updateServerCard(updatedServer);
    }
}


         

        
