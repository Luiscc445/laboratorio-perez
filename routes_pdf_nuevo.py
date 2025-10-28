# ============================================
# RUTAS DE PDFs - Agregar a routes.py
# ============================================

from flask import send_file, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.pdf_manager import PDFManager
from app.models import Resultado
from app import db
import os

# Inicializar gestor de PDFs
pdf_manager = None

def init_pdf_manager(app):
    global pdf_manager
    upload_folder = app.config.get('UPLOAD_FOLDER', 'app/uploads/resultados')
    pdf_manager = PDFManager(upload_folder)

# Llamar esto en create_app()
# init_pdf_manager(app)

@app.route('/resultados/subir', methods=['POST'])
@login_required
def subir_resultado():
    """Sube un nuevo resultado con PDF"""
    if not current_user.is_admin:
        flash('No tienes permiso para realizar esta acción.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Obtener datos del formulario
        numero_orden = request.form.get('numero_orden')
        paciente_nombre = request.form.get('paciente_nombre')
        paciente_ci = request.form.get('paciente_ci')
        fecha_muestra = request.form.get('fecha_muestra')
        
        # Validar datos
        if not all([numero_orden, paciente_nombre, paciente_ci, fecha_muestra]):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('admin_resultados'))
        
        # Obtener archivo PDF
        if 'archivo_pdf' not in request.files:
            flash('No se seleccionó ningún archivo PDF.', 'error')
            return redirect(url_for('admin_resultados'))
        
        file = request.files['archivo_pdf']
        
        # Guardar PDF usando el gestor
        success, filepath, error = pdf_manager.save_pdf(file, numero_orden)
        
        if not success:
            flash(f'Error al guardar PDF: {error}', 'error')
            return redirect(url_for('admin_resultados'))
        
        # Crear registro en la base de datos
        resultado = Resultado(
            numero_orden=numero_orden,
            paciente_nombre=paciente_nombre,
            paciente_ci=paciente_ci,
            fecha_muestra=fecha_muestra,
            archivo_pdf=filepath,
            medico_id=current_user.id
        )
        
        db.session.add(resultado)
        db.session.commit()
        
        flash(f'Resultado {numero_orden} guardado exitosamente.', 'success')
        return redirect(url_for('admin_resultados'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar resultado: {str(e)}', 'error')
        current_app.logger.error(f'Error en subir_resultado: {e}')
        return redirect(url_for('admin_resultados'))


@app.route('/resultados/descargar/<int:resultado_id>')
@login_required
def descargar(resultado_id):
    """Descarga un PDF de resultado"""
    try:
        # Obtener resultado
        resultado = Resultado.query.get_or_404(resultado_id)
        
        # Verificar permisos
        if not current_user.is_admin and resultado.medico_id != current_user.id:
            flash('No tienes permiso para descargar este resultado.', 'error')
            return redirect(url_for('index'))
        
        # Obtener ruta completa del archivo
        full_path = pdf_manager.get_full_path(resultado.archivo_pdf)
        
        # Verificar que el archivo existe
        if not full_path:
            flash('ERROR: El archivo PDF no existe en el servidor.', 'error')
            current_app.logger.error(f'Archivo no encontrado: {resultado.archivo_pdf}')
            
            # Eliminar registro huérfano si eres admin
            if current_user.is_admin:
                try:
                    numero_orden = resultado.numero_orden
                    db.session.delete(resultado)
                    db.session.commit()
                    flash(f'Registro {numero_orden} eliminado (archivo no encontrado).', 'warning')
                    current_app.logger.info(f'Registro huérfano eliminado: {numero_orden}')
                except Exception as e:
                    flash('Error al eliminar el registro.', 'error')
                    current_app.logger.error(f'Error al eliminar: {e}')
            
            return redirect(url_for('admin_resultados' if current_user.is_admin else 'index'))
        
        # Generar nombre para descarga
        download_name = f"{resultado.numero_orden}_{resultado.paciente_nombre}.pdf"
        download_name = secure_filename(download_name)
        
        # Enviar archivo
        return send_file(
            str(full_path),
            as_attachment=True,
            download_name=download_name,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        flash(f'Error al descargar el archivo: {str(e)}', 'error')
        current_app.logger.error(f'Error en descargar: {e}')
        return redirect(url_for('admin_resultados' if current_user.is_admin else 'index'))


@app.route('/resultados/eliminar/<int:resultado_id>', methods=['POST'])
@login_required
def eliminar_resultado(resultado_id):
    """Elimina un resultado y su PDF"""
    if not current_user.is_admin:
        flash('No tienes permiso para realizar esta acción.', 'error')
        return redirect(url_for('index'))
    
    try:
        resultado = Resultado.query.get_or_404(resultado_id)
        numero_orden = resultado.numero_orden
        
        # Eliminar archivo PDF
        pdf_manager.delete_pdf(resultado.archivo_pdf)
        
        # Eliminar registro de BD
        db.session.delete(resultado)
        db.session.commit()
        
        flash(f'Resultado {numero_orden} eliminado exitosamente.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar resultado: {str(e)}', 'error')
        current_app.logger.error(f'Error en eliminar_resultado: {e}')
    
    return redirect(url_for('admin_resultados'))


@app.route('/resultados/info/<int:resultado_id>')
@login_required
def info_pdf(resultado_id):
    """Obtiene información del PDF"""
    resultado = Resultado.query.get_or_404(resultado_id)
    
    if not current_user.is_admin and resultado.medico_id != current_user.id:
        return {'error': 'No autorizado'}, 403
    
    info = pdf_manager.get_pdf_info(resultado.archivo_pdf)
    
    if info:
        return {
            'numero_orden': resultado.numero_orden,
            'paciente': resultado.paciente_nombre,
            'pdf_info': info
        }
    else:
        return {'error': 'No se pudo obtener información del PDF'}, 404
