/**
 * Gestión de Pacientes - Laboratorio Pérez
 * Event listeners para modales y acciones de pacientes
 */

document.addEventListener('DOMContentLoaded', function() {
    // Event delegation para botones de ver
    document.querySelectorAll('.btn-ver').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const id = this.dataset.id;
            fetch(`/paciente/${id}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('verID').textContent = data.id;
                    document.getElementById('verNombre').textContent = data.nombre;
                    document.getElementById('verCI').textContent = data.ci;
                    document.getElementById('verTelefono').textContent = data.telefono;
                    document.getElementById('verEmail').textContent = data.email;
                    document.getElementById('verFecha').textContent = data.fecha_registro;
                    new bootstrap.Modal(document.getElementById('modalVer')).show();
                })
                .catch(error => {
                    console.error('Error al cargar datos del paciente:', error);
                    alert('Error al cargar los datos del paciente');
                });
        });
    });

    // Event delegation para botones de editar
    document.querySelectorAll('.btn-editar').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const id = this.dataset.id;
            const nombre = this.dataset.nombre;
            const ci = this.dataset.ci;
            const telefono = this.dataset.telefono;
            const email = this.dataset.email;

            document.getElementById('editID').value = id;
            document.getElementById('editNombre').value = nombre;
            document.getElementById('editCI').value = ci;
            document.getElementById('editTelefono').value = telefono;
            document.getElementById('editEmail').value = email;
            document.getElementById('formEditar').action = `/paciente/editar/${id}`;
            new bootstrap.Modal(document.getElementById('modalEditar')).show();
        });
    });

    // Event delegation para botones de eliminar
    document.querySelectorAll('.btn-eliminar').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const id = this.dataset.id;
            const nombre = this.dataset.nombre;

            document.getElementById('eliminarNombre').textContent = nombre;
            document.getElementById('formEliminar').action = `/paciente/eliminar/${id}`;
            new bootstrap.Modal(document.getElementById('modalEliminar')).show();
        });
    });
});
