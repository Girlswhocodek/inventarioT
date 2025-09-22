
const API_BASE = '';

// Función para hacer requests autenticados
const fetchWithAuth = async (url, options = {}) => {
    const token = localStorage.getItem('access_token');
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(`${API_BASE}${url}`, {
            ...options,
            headers,
        });
        
        if (response.status === 401) {
            localStorage.removeItem('access_token');
            window.location.href = '/login';
            return null;
        }
        
        return response;
    } catch (error) {
        console.error('Error en la petición:', error);
        throw error;
    }
};

// Función para login
const login = async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    formData.append('grant_type', 'password');
    
    const response = await fetch('/auth/token', {
        method: 'POST',
        body: formData
    });
    
    if (!response.ok) {
        throw new Error('Credenciales incorrectas');
    }
    
    return response.json();
};

// Función para búsqueda
const buscar = async (query, nivel = '') => {
    let url = `/buscar?q=${encodeURIComponent(query)}`;
    if (nivel) url += `&nivel=${nivel}`;
    
    const response = await fetchWithAuth(url);
    if (!response) return null;
    
    return response.json();
};

// Función para obtener KPIs
const obtenerKPIs = async () => {
    const response = await fetchWithAuth('/kpis');
    if (!response) return null;
    
    return response.json();
};

// Exportar funciones
window.api = {
    fetchWithAuth,
    login,
    buscar,
    obtenerKPIs
};
