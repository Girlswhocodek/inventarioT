// kpi.js - Script para integrar el dashboard con el backend

let allData = [];
let filteredData = [];
let currentPage = 1;
const rowsPerPage = 10;
let selectedRecord = null;

// API Base URL
const API_BASE = '/api/kpis';

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initializeFilters();
    loadInitialData();
    setupEventListeners();
});

function initializeFilters() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('singleDate').value = today;
    
    document.getElementById('filterType').addEventListener('change', function() {
        updateFilterVisibility(this.value);
    });
}

function setupEventListeners() {
    // Cerrar modal al hacer clic fuera
    window.onclick = function(event) {
        const modal = document.getElementById('detailModal');
        if (event.target === modal) {
            closeModal();
        }
    };
    
    // Enter key en los inputs de filtro
    const filterInputs = document.querySelectorAll('.filter-group input');
    filterInputs.forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                applyFilters();
            }
        });
    });
}

function updateFilterVisibility(type) {
    document.getElementById('singleDayFilter').style.display = type === 'day' ? 'block' : 'none';
    document.getElementById('startDateFilter').style.display = type === 'range' ? 'block' : 'none';
    document.getElementById('endDateFilter').style.display = type === 'range' ? 'block' : 'none';
    document.getElementById('monthFilter').style.display = type === 'month' ? 'block' : 'none';
}

async function loadInitialData() {
    try {
        showLoading(true);
        const today = new Date().toISOString().split('T')[0];
        const params = new URLSearchParams({
            filter_type: 'day',
            single_date: today
        });
        
        const response = await fetch(`${API_BASE}/data?${params}`);
        
        if (!response.ok) {
            throw new Error('Error al cargar los datos');
        }
        
        const data = await response.json();
        allData = data;
        filteredData = [...allData];
        currentPage = 1;
        renderTable();
    } catch (error) {
        console.error('Error:', error);
        showError('Error al cargar los datos iniciales');
    } finally {
        showLoading(false);
    }
}

async function applyFilters() {
    try {
        showLoading(true);
        
        const filterType = document.getElementById('filterType').value;
        const statusFilter = document.getElementById('statusFilter').value;
        const schemaFilter = document.getElementById('schemaFilter').value;
        
        const params = new URLSearchParams({
            filter_type: filterType
        });
        
        // Agregar parámetros de fecha según el tipo de filtro
        if (filterType === 'day') {
            const singleDate = document.getElementById('singleDate').value;
            if (singleDate) {
                params.append('single_date', singleDate);
            }
        } else if (filterType === 'range') {
            const startDate = document.getElementById('startDate').value;
            const endDate = document.getElementById('endDate').value;
            if (startDate && endDate) {
                params.append('start_date', startDate);
                params.append('end_date', endDate);
            } else {
                showError('Debe seleccionar fecha de inicio y fin');
                return;
            }
        } else if (filterType === 'month') {
            const month = document.getElementById('monthSelect').value;
            if (month) {
                params.append('month', month);
            }
        }
        
        // Agregar filtros adicionales
        if (statusFilter) {
            params.append('status', statusFilter);
        }
        if (schemaFilter) {
            params.append('schema', schemaFilter);
        }
        
        const response = await fetch(`${API_BASE}/data?${params}`);
        
        if (!response.ok) {
            throw new Error('Error al aplicar filtros');
        }
        
        const data = await response.json();
        allData = data;
        filteredData = [...allData];
        currentPage = 1;
        renderTable();
        
    } catch (error) {
        console.error('Error:', error);
        showError('Error al aplicar los filtros');
    } finally {
        showLoading(false);
    }
}

function resetFilters() {
    document.getElementById('filterType').value = 'day';
    document.getElementById('singleDate').value = new Date().toISOString().split('T')[0];
    document.getElementById('statusFilter').value = '';
    document.getElementById('schemaFilter').value = '';
    document.getElementById('startDate').value = '';
    document.getElementById('endDate').value = '';
    document.getElementById('monthSelect').value = '';
    updateFilterVisibility('day');
    loadInitialData();
}

function renderTable() {
    const tbody = document.getElementById('dataTable');
    tbody.innerHTML = '';
    
    if (filteredData.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="13" style="text-align: center; padding: 40px; color: #999;">
                    <i class="fas fa-inbox" style="font-size: 48px; margin-bottom: 10px;"></i>
                    <div>No se encontraron registros</div>
                </td>
            </tr>
        `;
        updatePagination();
        return;
    }
    
    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const pageData = filteredData.slice(start, end);
    
    pageData.forEach((item) => {
        const row = document.createElement('tr');
        row.className = item.estado;
        row.onclick = () => showDetail(item);
        row.style.cursor = 'pointer';
        
        row.innerHTML = `
            <td>${formatDate(item.fecha)}</td>
            <td>${item.trafico}</td>
            <td>${item.esquema}</td>
            <td>${item.tablas}</td>
            <td>${item.tipo}</td>
            <td><span class="status-badge status-${item.estado}">${formatStatus(item.estado)}</span></td>
            <td>${item.diferencia}</td>
            <td>${formatNumber(item.cant_archivos_cg)}</td>
            <td>${formatNumber(item.cnt_regis_cg)}</td>
            <td>${formatNumber(item.cant_archivos_db)}</td>
            <td>${formatNumber(item.cant_regis_db)}</td>
            <td>${formatNumber(item.diferencia_registros)}</td>
            <td>${item.fecha_reproceso ? formatDate(item.fecha_reproceso) : '-'}</td>
        `;
        
        tbody.appendChild(row);
    });
    
    updatePagination();
}

function updatePagination() {
    const totalPages = Math.ceil(filteredData.length / rowsPerPage);
    document.getElementById('pageInfo').textContent = `Página ${currentPage} de ${Math.max(totalPages, 1)}`;
    document.getElementById('prevBtn').disabled = currentPage === 1;
    document.getElementById('nextBtn').disabled = currentPage >= totalPages || totalPages === 0;
}

function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        renderTable();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function nextPage() {
    const totalPages = Math.ceil(filteredData.length / rowsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        renderTable();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function showDetail(record) {
    selectedRecord = record;
    const modal = document.getElementById('detailModal');
    const content = document.getElementById('detailContent');
    
    content.innerHTML = `
        <div class="detail-item">
            <div class="detail-label">Fecha</div>
            <div class="detail-value">${formatDate(record.fecha)}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Tráfico</div>
            <div class="detail-value">${record.trafico}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Esquema</div>
            <div class="detail-value">${record.esquema}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Tablas</div>
            <div class="detail-value">${record.tablas}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Tipo</div>
            <div class="detail-value">${record.tipo}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Estado</div>
            <div class="detail-value"><span class="status-badge status-${record.estado}">${formatStatus(record.estado)}</span></div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Diferencia</div>
            <div class="detail-value">${record.diferencia}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Archivos CG</div>
            <div class="detail-value">${formatNumber(record.cant_archivos_cg)}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Registros CG</div>
            <div class="detail-value">${formatNumber(record.cnt_regis_cg)}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Archivos DB</div>
            <div class="detail-value">${formatNumber(record.cant_archivos_db)}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Registros DB</div>
            <div class="detail-value">${formatNumber(record.cant_regis_db)}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Diferencia Registros</div>
            <div class="detail-value">${formatNumber(record.diferencia_registros)}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Fecha Reproceso</div>
            <div class="detail-value">${record.fecha_reproceso ? formatDate(record.fecha_reproceso) : 'No aplica'}</div>
        </div>
    `;
    
    modal.classList.add('active');
}

function closeModal() {
    document.getElementById('detailModal').classList.remove('active');
}

async function exportToExcel() {
    try {
        showLoading(true);
        
        const filterType = document.getElementById('filterType').value;
        const statusFilter = document.getElementById('statusFilter').value;
        const schemaFilter = document.getElementById('schemaFilter').value;
        
        const payload = {
            filter_type: filterType,
            status: statusFilter,
            schema: schemaFilter
        };
        
        // Agregar parámetros de fecha
        if (filterType === 'day') {
            payload.single_date = document.getElementById('singleDate').value;
        } else if (filterType === 'range') {
            payload.start_date = document.getElementById('startDate').value;
            payload.end_date = document.getElementById('endDate').value;
        } else if (filterType === 'month') {
            payload.month = document.getElementById('monthSelect').value;
        }
        
        const response = await fetch(`${API_BASE}/export/excel`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error('Error al exportar');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `reporte_kpis_${new Date().toISOString().split('T')[0]}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showSuccess('Excel descargado exitosamente');
    } catch (error) {
        console.error('Error:', error);
        showError('Error al exportar a Excel');
    } finally {
        showLoading(false);
    }
}

async function exportDetailToExcel() {
    if (!selectedRecord) return;
    
    try {
        showLoading(true);
        
        const response = await fetch(`${API_BASE}/export/detail`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ record_id: selectedRecord.id })
        });
        
        if (!response.ok) {
            throw new Error('Error al exportar detalle');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `detalle_${selectedRecord.fecha}_${selectedRecord.esquema}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showSuccess('Detalle descargado exitosamente');
    } catch (error) {
        console.error('Error:', error);
        showError('Error al exportar detalle');
    } finally {
        showLoading(false);
    }
}

// Utility Functions
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}

function formatNumber(num) {
    if (num === null || num === undefined) return '0';
    return num.toLocaleString('es-ES');
}

function formatStatus(status) {
    const statusMap = {
        'igual': 'IGUAL',
        'faltante-bd': 'FALTANTE BD',
        'faltante-cg': 'FALTANTE CG'
    };
    return statusMap[status] || status.toUpperCase();
}

function showLoading(show) {
    // Implementar overlay de carga
    let loader = document.getElementById('globalLoader');
    if (!loader) {
        loader = document.createElement('div');
        loader.id = 'globalLoader';
        loader.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        `;
        loader.innerHTML = '<i class="fas fa-spinner fa-spin" style="font-size: 48px; color: white;"></i>';
        document.body.appendChild(loader);
    }
    loader.style.display = show ? 'flex' : 'none';
}

function showError(message) {
    showNotification(message, 'error');
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 10000;
        animation: slideIn 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        background: ${type === 'error' ? '#e74c3c' : '#27ae60'};
    `;
    notification.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'check-circle'}"></i>
        ${message}
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Agregar animaciones CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);