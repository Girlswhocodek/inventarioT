
const servidoresData = [
            {
                id: 1,
                nombre: "SERVER-WEB-01",
                ip: "192.168.1.10",
                tecnologia: "VMware",
                estado: "activo",
                cpu_nucleos: 8,
                ram_gb: 32,
                almacenamiento_gb: 500,
                fabricante: "Dell",
                modelo: "PowerEdge R740",
                particionado: true,
                ubicacion: "Datacenter Principal",
                responsable: "Juan Pérez",
                arquitectura: "x64"
            },
            {
                id: 2,
                nombre: "SERVER-DB-01",
                ip: "192.168.1.20",
                tecnologia: "Hyper-V",
                estado: "activo",
                cpu_nucleos: 16,
                ram_gb: 64,
                almacenamiento_gb: 1000,
                fabricante: "HP",
                modelo: "ProLiant DL380",
                particionado: false,
                ubicacion: "Sala de Servidores A",
                responsable: "María García",
                arquitectura: "x64"
            },
            {
                id: 3,
                nombre: "SERVER-TEST-01",
                ip: "192.168.1.30",
                tecnologia: "Docker",
                estado: "inactivo",
                cpu_nucleos: 4,
                ram_gb: 16,
                almacenamiento_gb: 250,
                fabricante: "IBM",
                modelo: "System x3650",
                particionado: true,
                ubicacion: "Lab de Desarrollo",
                responsable: "Carlos López",
                arquitectura: "x64"
            },
        

            { 
                id: 4, 
                nombre: 'Servidor de Desarrollo', 
                ip: '192.168.1.40', 
                estado: 'activo', 
                cpu_nucleos: 4, 
                ram_gb: 8, 
                almacenamiento_gb: 250,
                ubicacion: 'Oficina Desarrollo',
                tecnologia: 'Virtual',
                fabricante: 'Dell',
                modelo: 'PowerEdge R640',
                numero_serie: 'SN456789',
                arquitectura: 'x64',
                particionado: true,
                fecha_instalacion_so: '2023-06-10',
                responsable: 'Ana Rodríguez',
                fecha_creacion: '2023-06-05T08:45:00',
                fecha_actualizacion: '2023-11-15T10:20:00'
            },
        { 
                id: 5, 
                nombre: 'Servidor de Testing', 
                ip: '192.168.1.50', 
                    estado: 'mantenimiento', 
                    cpu_nucleos: 4, 
                    ram_gb: 8, 
                    almacenamiento_gb: 300,
                    ubicacion: 'Oficina Calidad',
                    tecnologia: 'Virtual',
                    fabricante: 'HP',
                    modelo: 'ProLiant DL360',
                    numero_serie: 'SN567890',
                    arquitectura: 'x64',
                    particionado: true,
                    fecha_instalacion_so: '2023-07-22',
                    responsable: 'Pedro Martínez',
                    fecha_creacion: '2023-07-18T13:30:00',
                    fecha_actualizacion: '2023-11-10T09:15:00'
                },
                { 
                    id: 6, 
                    nombre: 'Servidor de Archivos', 
                    ip: '192.168.1.60', 
                    estado: 'activo', 
                    cpu_nucleos: 8, 
                    ram_gb: 16, 
                    almacenamiento_gb: 4000,
                    ubicacion: 'Data Center Principal',
                    tecnologia: 'Físico',
                    fabricante: 'Dell',
                    modelo: 'PowerEdge R740xd',
                    numero_serie: 'SN678901',
                    arquitectura: 'x64',
                    particionado: false,
                    fecha_instalacion_so: '2023-04-05',
                    responsable: 'Laura Sánchez',
                    fecha_creacion: '2023-03-30T11:20:00',
                    fecha_actualizacion: '2023-11-12T16:45:00'
                },
                { 
                    id: 7, 
                    nombre: 'Servidor de Correo', 
                    ip: '192.168.1.70', 
                    estado: 'activo', 
                    cpu_nucleos: 8, 
                    ram_gb: 16, 
                    almacenamiento_gb: 500,
                    ubicacion: 'Data Center Secundario',
                    tecnologia: 'Virtual',
                    fabricante: 'HP',
                    modelo: 'ProLiant DL380',
                    numero_serie: 'SN789012',
                    arquitectura: 'x64',
                    particionado: true,
                    fecha_instalacion_so: '2023-02-14',
                    responsable: 'Miguel Ángel Fernández',
                    fecha_creacion: '2023-02-10T09:00:00',
                    fecha_actualizacion: '2023-11-08T14:30:00'
                },
                { 
                    id: 8, 
                    nombre: 'Servidor Legacy', 
                    ip: '192.168.1.80', 
                    estado: 'inactivo', 
                    cpu_nucleos: 2, 
                    ram_gb: 4, 
                    almacenamiento_gb: 100,
                    ubicacion: 'Almacén',
                    tecnologia: 'Físico',
                    fabricante: 'IBM',
                    modelo: 'System x3250',
                    numero_serie: 'SN890123',
                    arquitectura: 'x86',
                    particionado: false,
                    fecha_instalacion_so: '2020-11-30',
                    responsable: 'Sofía Hernández',
                    fecha_creacion: '2020-11-25T15:45:00',
                    fecha_actualizacion: '2023-10-20T12:10:00'
                }

];

const sistemasOperativos = {
            1: [
                { id: 1, nombre: "Ubuntu Server 20.04", version: "20.04.3", tipo: "Principal" },
                { id: 2, nombre: "Windows Server 2019", version: "1809", tipo: "Secundario" }
            ],
            2: [
                { id: 3, nombre: "CentOS 8", version: "8.4", tipo: "Principal" }
            ],
            3: [
                { id: 4, nombre: "Debian 11", version: "11.2", tipo: "Principal" }
            ]
        };

        const instanciasBd = {
            1: [
                { id: 1, nombre: "MySQL-PROD", motor: "MySQL", version: "8.0.27", puerto: 3306, estado: "activo" },
                { id: 2, nombre: "Redis-Cache", motor: "Redis", version: "6.2.6", puerto: 6379, estado: "activo" }
            ],
            2: [
                { id: 3, nombre: "PostgreSQL-MAIN", motor: "PostgreSQL", version: "13.5", puerto: 5432, estado: "activo" },
                { id: 4, nombre: "MongoDB-Analytics", motor: "MongoDB", version: "5.0.3", puerto: 27017, estado: "activo" }
            ],
            3: []
        };

        const discos = {
            1: [
                { id: 1, dispositivo: "/dev/sda1", tamaño_gb: 100, tipo: "SSD", punto_montaje: "/" },
                { id: 2, dispositivo: "/dev/sda2", tamaño_gb: 400, tipo: "SSD", punto_montaje: "/var" }
            ],
            2: [
                { id: 3, dispositivo: "/dev/sda1", tamaño_gb: 200, tipo: "NVMe", punto_montaje: "/" },
                { id: 4, dispositivo: "/dev/sdb1", tamaño_gb: 800, tipo: "HDD", punto_montaje: "/data" }
            ],
            3: [
                { id: 5, dispositivo: "/dev/sda1", tamaño_gb: 250, tipo: "SSD", punto_montaje: "/" }
            ],
            4: [
                { id: 6, dispositivo: "/dev/sda1", tamaño_gb: 500, tipo: "NVMe", punto_montaje: "/", usado_gb: 200 },
                { id: 7, dispositivo: "/dev/sdb1", tamaño_gb: 1500, tipo: "SSD", punto_montaje: "/oradata", usado_gb: 750 }
            ]
        };

        // Función para obtener datos de servidores (simula API)
async function obtenerServidores() {
    return new Promise((resolve) => {
        // Simular delay de red
        setTimeout(() => {
            resolve(servidoresData);
        }, 500);
    });
}

// Función para obtener sistemas operativos de un servidor
async function obtenerSistemasOperativos(serverId) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(sistemasOperativos[serverId] || []);
        }, 300);
    });
}

// Función para obtener instancias de BD de un servidor
async function obtenerInstanciasBD(serverId) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(instanciasBd[serverId] || []);
        }, 300);
    });
}

// Función para obtener discos de un servidor
async function obtenerDiscos(serverId) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(discos[serverId] || []);
        }, 300);
    });
}

// Exportar funciones para uso en otros archivos
if (typeof module !== 'undefined' && module.exports) {
    // Para Node.js/Testing
    module.exports = {
        servidoresData,
        sistemasOperativos,
        instanciasBd,
        discos,
        obtenerServidores,
        obtenerSistemasOperativos,
        obtenerInstanciasBD,
        obtenerDiscos
    };
}
