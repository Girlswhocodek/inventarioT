
const layoutHTML = `
<div class="sidebar" id="sidebar">
    <div class="logo">
        <i class="fas fa-box-open"></i>
        <h1>Inventario</h1>
    </div>

    <div class="nav-item" onclick="window.location.href='/dashboard'">
        <i class="fas fa-home"></i>
        <span>Dashboard</span>
    </div>

    <div class="nav-item active" onclick="window.location.href='/servidores'">
        <i class="fas fa-server"></i>
        <span>Servidores</span>
    </div>

    <div class="nav-item" onclick="window.location.href='/sistemas-operativos'">
        <i class="fab fa-windows"></i>
        <span>Sistemas Operativos</span>
    </div>

    <div class="nav-item" onclick="window.location.href='/bases-datos'">
        <i class="fas fa-database"></i>
        <span>Bases de Datos</span>
    </div>

    <div class="nav-item" onclick="window.location.href='/gestion'">
        <i class="fas fa-tools"></i>
        <span>Gestión</span>
    </div>

    <div class="nav-item" onclick="window.location.href='/kpis'">
        <i class="fas fa-chart-line"></i>
        <span>KPIs</span>
    </div>

    <div class="nav-item" onclick="window.location.href='/configuracion'">
        <i class="fas fa-cog"></i>
        <span>Configuración</span>
    </div>
</div>
`;
const userInfoHTML = `
    <div class="user-info" id="userInfoPanel">
        <i class="fas fa-user-circle" style="font-size: 32px; color: #4361ee; margin-right: 10px;"></i>
        <div>
            <div id="usernameDisplay">Administrador</div>
            <small>Administrador</small>
        </div>
        
        <div class="user-panel" id="userPanel">
            <div class="user-panel-menu">
                <div class="user-panel-item">
                    <i class="fas fa-user"></i>
                    <span>Mi Perfil</span>
                </div>
                <div class="user-panel-item">
                    <i class="fas fa-cog"></i>
                    <span>Configuración</span>
                </div>
                <div class="user-panel-item">
                    <i class="fas fa-bell"></i>
                    <span>Notificaciones</span>
                </div>
                <div class="user-panel-divider"></div>
                <div class="user-panel-item" id="logoutButton">
                    <i class="fas fa-sign-out-alt"></i>
                    <span>Cerrar Sesión</span>
                </div>
            </div>
        </div>
    </div>
`

// Esta función se encarga de inyectar el HTML en la página
document.addEventListener("DOMContentLoaded", () => {
    const layoutContainer = document.getElementById("layout-container");
    if (layoutContainer) {
        layoutContainer.innerHTML = layoutHTML;
    }
    const userInfoContainer = document.getElementById("user-info-container");
    if (userInfoContainer) {
        userInfoContainer.innerHTML = userInfoHTML;
    }
});