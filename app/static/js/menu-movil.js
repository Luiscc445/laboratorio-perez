/**
 * Menu Móvil - Laboratorio Pérez
 * Asegura el correcto funcionamiento del botón hamburguesa en dispositivos móviles
 */

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar el menú móvil cuando el DOM esté listo
    initMobileMenu();

    // Re-inicializar si la ventana cambia de tamaño
    window.addEventListener('resize', debounce(initMobileMenu, 250));
});

/**
 * Inicializa el menú móvil y asegura que el botón hamburguesa funcione
 */
function initMobileMenu() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    if (!navbarToggler || !navbarCollapse) {
        console.warn('No se encontraron elementos del navbar');
        return;
    }

    // Asegurar que Bootstrap inicialice el collapse
    if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
        // Verificar si ya existe una instancia de Collapse
        let collapseInstance = bootstrap.Collapse.getInstance(navbarCollapse);

        if (!collapseInstance) {
            // Crear nueva instancia de Collapse
            collapseInstance = new bootstrap.Collapse(navbarCollapse, {
                toggle: false
            });
        }

        // Agregar evento de clic manual como respaldo
        navbarToggler.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            // Toggle del menú
            if (navbarCollapse.classList.contains('show')) {
                collapseInstance.hide();
            } else {
                collapseInstance.show();
            }
        });

        console.log('✓ Menú móvil inicializado correctamente');
    } else {
        console.error('Bootstrap no está cargado correctamente');

        // Fallback: implementación manual del toggle
        navbarToggler.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            navbarCollapse.classList.toggle('show');
        });

        console.log('✓ Menú móvil inicializado con fallback manual');
    }

    // Cerrar el menú al hacer clic en un enlace (solo en móvil)
    const navLinks = navbarCollapse.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth < 992) { // Bootstrap lg breakpoint
                const collapseInstance = bootstrap.Collapse.getInstance(navbarCollapse);
                if (collapseInstance && navbarCollapse.classList.contains('show')) {
                    collapseInstance.hide();
                }
            }
        });
    });
}

/**
 * Función debounce para optimizar el rendimiento
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Cerrar el menú al hacer clic fuera de él
 */
document.addEventListener('click', function(event) {
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navbarToggler = document.querySelector('.navbar-toggler');

    if (!navbarCollapse || !navbarToggler) return;

    // Si el clic fue fuera del navbar y el menú está abierto
    if (!event.target.closest('.navbar') && navbarCollapse.classList.contains('show')) {
        if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
            const collapseInstance = bootstrap.Collapse.getInstance(navbarCollapse);
            if (collapseInstance) {
                collapseInstance.hide();
            }
        } else {
            navbarCollapse.classList.remove('show');
        }
    }
});
