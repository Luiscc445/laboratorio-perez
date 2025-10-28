# Fix para routes.py - Agregar esta función reemplazando la función descargar existente

import os
from flask import flash, redirect, url_for, send_file
from flask_login import login_required, current_user

@app.route('/resultados/descargar/<int:resultado_id>')
@login_required
def descargar(resultado_id):
    from app.models import Resultado
    
    resultado = Resultado.query.get_or_404(resultado_id)
    
    # Verificar permisos
    if not current_user.is_admin and resultado.medico_id != current_user.id:
        flash('No tienes permiso para descargar este resultado.', 'error')
        return redirect(url_for('index'))
    
    # Construir ruta completa del archivo
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_completa = os.path.join(base_dir, resultado.archivo_pdf)
    
    # Verificar que el archivo existe
    if not os.path.exists(ruta_completa):
        flash(f'ERROR: El archivo PDF no existe en el servidor.', 'error')
        app.logger.error(f'Archivo no encontrado: {ruta_completa}')
        app.logger.error(f'Registro ID: {resultado.id}, Orden: {resultado.numero_orden}')
        
        # Si eres admin, eliminar el registro huérfano automáticamente
        if current_user.is_admin:
            try:
                numero_orden = resultado.numero_orden
                db.session.delete(resultado)
                db.session.commit()
                flash(f'Registro {numero_orden} eliminado (archivo no encontrado).', 'warning')
                app.logger.info(f'Registro huérfano eliminado: {numero_orden}')
            except Exception as e:
                flash('Error al eliminar el registro.', 'error')
                app.logger.error(f'Error al eliminar registro: {e}')
        
        # Redirigir según el rol
        if current_user.is_admin:
            return redirect(url_for('admin_resultados'))
        else:
            return redirect(url_for('index'))
    
    # Si el archivo existe, descargarlo
    try:
        return send_file(ruta_completa, as_attachment=True)
    except Exception as e:
        flash(f'Error al descargar el archivo: {str(e)}', 'error')
        app.logger.error(f'Error en descarga: {e}')
        return redirect(url_for('admin_resultados' if current_user.is_admin else 'index'))
