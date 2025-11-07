from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Paciente, Resultado, Prueba
from app.utils import admin_required
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from sqlalchemy import func, extract
import os
import random
import string
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

main = Blueprint('main', __name__)

# Definir ruta base absoluta para archivos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
PRUEBAS_UPLOAD_DIR = os.path.join(UPLOAD_DIR, 'pruebas')

def generar_codigo_acceso():
    """Genera un código aleatorio de 8 caracteres"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@main.route('/')
def index():
    return render_template('publico/index.html')

@main.route('/portal-resultados')
def portal_resultados():
    return render_template('publico/portal_resultados.html')

@main.route('/catalogo-pruebas')
def catalogo_pruebas():
    # Obtener todas las pruebas ordenadas por categoría y nombre
    pruebas = Prueba.query.order_by(Prueba.categoria, Prueba.nombre).all()

    # Organizar pruebas por categoría
    pruebas_por_categoria = {}
    for prueba in pruebas:
        categoria = prueba.categoria or 'General'
        if categoria not in pruebas_por_categoria:
            pruebas_por_categoria[categoria] = []
        pruebas_por_categoria[categoria].append(prueba)

    return render_template('publico/catalogo/lista_pruebas.html',
                         pruebas=pruebas,
                         pruebas_por_categoria=pruebas_por_categoria)

@main.route('/consultar-resultado', methods=['POST'])
def consultar_resultado():
    ci = request.form.get('ci')
    codigo = request.form.get('codigo')

    resultado = Resultado.query.filter_by(paciente_ci=ci, codigo_acceso=codigo).first()

    if resultado:
        return render_template('publico/ver_resultado.html', resultado=resultado)
    else:
        flash('CI o código de acceso incorrecto', 'danger')
        return redirect(url_for('main.portal_resultados'))

@main.route('/dashboard')
@admin_required
def dashboard():
    # Estadísticas básicas
    total_pacientes = Paciente.query.count()
    total_resultados = Resultado.query.count()
    total_pruebas = Prueba.query.count()

    # Pacientes registrados en los últimos 6 meses
    fecha_inicio = datetime.now() - timedelta(days=180)
    pacientes_por_mes = db.session.query(
        extract('month', Paciente.fecha_registro).label('mes'),
        func.count(Paciente.id).label('total')
    ).filter(Paciente.fecha_registro >= fecha_inicio).group_by('mes').all()

    # Resultados por mes en los últimos 6 meses
    resultados_por_mes = db.session.query(
        extract('month', Resultado.fecha_muestra).label('mes'),
        func.count(Resultado.id).label('total')
    ).filter(Resultado.fecha_muestra >= fecha_inicio).group_by('mes').all()

    # Top 5 pruebas más recientes del catálogo
    top_pruebas = db.session.query(
        Prueba.nombre,
        Prueba.precio
    ).order_by(Prueba.fecha_creacion.desc()).limit(5).all()

    # Estadísticas adicionales
    pacientes_este_mes = Paciente.query.filter(
        extract('month', Paciente.fecha_registro) == datetime.now().month,
        extract('year', Paciente.fecha_registro) == datetime.now().year
    ).count()

    resultados_este_mes = Resultado.query.filter(
        extract('month', Resultado.fecha_muestra) == datetime.now().month,
        extract('year', Resultado.fecha_muestra) == datetime.now().year
    ).count()

    # Preparar datos para gráficos
    meses_nombres = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    mes_actual = datetime.now().month

    # Últimos 6 meses
    ultimos_meses = []
    for i in range(5, -1, -1):
        mes_idx = (mes_actual - i - 1) % 12
        ultimos_meses.append(meses_nombres[mes_idx])

    # Crear arrays de datos para gráficos
    pacientes_data = [0] * 6
    resultados_data = [0] * 6

    for mes, total in pacientes_por_mes:
        mes_idx = int(mes)
        pos = 5 - ((mes_actual - mes_idx) % 12)
        if 0 <= pos < 6:
            pacientes_data[pos] = total

    for mes, total in resultados_por_mes:
        mes_idx = int(mes)
        pos = 5 - ((mes_actual - mes_idx) % 12)
        if 0 <= pos < 6:
            resultados_data[pos] = total

    return render_template('admin/dashboard.html',
                         total_pacientes=total_pacientes,
                         total_resultados=total_resultados,
                         total_pruebas=total_pruebas,
                         pacientes_este_mes=pacientes_este_mes,
                         resultados_este_mes=resultados_este_mes,
                         ultimos_meses=ultimos_meses,
                         pacientes_data=pacientes_data,
                         resultados_data=resultados_data,
                         top_pruebas=top_pruebas)

@main.route('/pacientes', methods=['GET', 'POST'])
@admin_required
def admin_pacientes():
    if request.method == 'POST':
        try:
            paciente = Paciente(
                nombre=request.form['nombre'],
                ci=request.form['ci'],
                telefono=request.form.get('telefono'),
                email=request.form.get('email')
            )
            db.session.add(paciente)
            db.session.commit()
            flash('Paciente registrado exitosamente', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('main.admin_pacientes'))
    pacientes = Paciente.query.order_by(Paciente.fecha_registro.desc()).all()
    return render_template('admin/pacientes.html', pacientes=pacientes, now=datetime.now())

@main.route('/paciente/<int:paciente_id>')
@admin_required
def ver_paciente(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    return jsonify({
        'id': paciente.id,
        'nombre': paciente.nombre,
        'ci': paciente.ci,
        'telefono': paciente.telefono or '-',
        'email': paciente.email or '-',
        'fecha_registro': paciente.fecha_registro.strftime('%d/%m/%Y %H:%M')
    })

@main.route('/paciente/editar/<int:paciente_id>', methods=['POST'])
@admin_required
def editar_paciente(paciente_id):
    try:
        paciente = Paciente.query.get_or_404(paciente_id)
        paciente.nombre = request.form['nombre']
        paciente.ci = request.form['ci']
        paciente.telefono = request.form.get('telefono')
        paciente.email = request.form.get('email')

        resultados = Resultado.query.filter_by(paciente_id=paciente_id).all()
        for resultado in resultados:
            resultado.paciente_nombre = paciente.nombre
            resultado.paciente_ci = paciente.ci

        db.session.commit()
        flash('Paciente y sus resultados actualizados exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('main.admin_pacientes'))

@main.route('/paciente/eliminar/<int:paciente_id>', methods=['POST'])
@admin_required
def eliminar_paciente(paciente_id):
    try:
        paciente = Paciente.query.get_or_404(paciente_id)
        nombre_paciente = paciente.nombre

        # Obtener todos los resultados del paciente
        resultados = Resultado.query.filter_by(paciente_id=paciente_id).all()

        # Eliminar archivos PDF físicos
        archivos_eliminados = 0
        for resultado in resultados:
            if resultado.archivo_pdf:
                try:
                    pdf_path = os.path.join(UPLOAD_DIR, resultado.archivo_pdf)
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
                        archivos_eliminados += 1
                except Exception as e:
                    print(f"Error eliminando archivo {resultado.archivo_pdf}: {e}")

        # SQLAlchemy eliminará automáticamente los resultados gracias a cascade='all, delete-orphan'
        db.session.delete(paciente)
        db.session.commit()

        flash(f'Paciente "{nombre_paciente}" eliminado exitosamente junto con {len(resultados)} resultado(s) y {archivos_eliminados} archivo(s) PDF', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar paciente: {str(e)}', 'danger')
        print(f"Error: {e}")

    return redirect(url_for('main.admin_pacientes'))

@main.route('/resultados', methods=['GET', 'POST'])
@admin_required
def admin_resultados():
    if request.method == 'POST':
        archivo_guardado = None
        try:
            archivo = request.files.get('archivo_pdf')
            filename = None

            if not archivo or not archivo.filename:
                flash('Debe seleccionar un archivo PDF', 'danger')
                return redirect(url_for('main.admin_resultados'))

            if not archivo.filename.endswith('.pdf'):
                flash('Solo se permiten archivos PDF', 'danger')
                return redirect(url_for('main.admin_resultados'))

            # Generar nombre de archivo seguro y único
            filename = secure_filename(f"{request.form['numero_orden']}_{archivo.filename}")

            # Asegurar que el directorio existe con permisos correctos
            os.makedirs(UPLOAD_DIR, exist_ok=True)

            # Ruta completa del archivo
            filepath = os.path.join(UPLOAD_DIR, filename)

            # Guardar archivo
            archivo.save(filepath)
            archivo_guardado = filepath

            # VERIFICACIÓN CRÍTICA: Asegurar que el archivo existe y tiene contenido
            if not os.path.exists(filepath):
                raise Exception(f"El archivo no se guardó correctamente en: {filepath}")

            file_size = os.path.getsize(filepath)
            if file_size == 0:
                os.remove(filepath)
                raise Exception("El archivo PDF está vacío")

            print(f"✓ PDF guardado exitosamente: {filepath} ({file_size} bytes)")

            # Continuar con el registro en base de datos
            fecha_str = request.form.get('fecha_muestra')
            fecha_muestra = datetime.strptime(fecha_str, '%Y-%m-%d').date() if fecha_str else None

            paciente_id = request.form.get('paciente_id')
            if not paciente_id:
                # Si falla, eliminar el archivo guardado
                if archivo_guardado and os.path.exists(archivo_guardado):
                    os.remove(archivo_guardado)
                flash('Debe seleccionar un paciente', 'danger')
                return redirect(url_for('main.admin_resultados'))

            paciente = Paciente.query.get(int(paciente_id))
            if not paciente:
                # Si falla, eliminar el archivo guardado
                if archivo_guardado and os.path.exists(archivo_guardado):
                    os.remove(archivo_guardado)
                flash('Paciente no encontrado', 'danger')
                return redirect(url_for('main.admin_resultados'))

            codigo_acceso = generar_codigo_acceso()
            resultado = Resultado(
                numero_orden=request.form['numero_orden'],
                paciente_id=paciente.id,
                paciente_nombre=paciente.nombre,
                paciente_ci=paciente.ci,
                fecha_muestra=fecha_muestra,
                archivo_pdf=filename,
                codigo_acceso=codigo_acceso
            )
            db.session.add(resultado)
            db.session.commit()

            print(f"✓ Resultado registrado en BD: ID={resultado.id}, Código={codigo_acceso}")
            flash(f'Resultado guardado. Código de acceso: {codigo_acceso}', 'success')

        except Exception as e:
            db.session.rollback()
            # Si hubo error y el archivo se guardó, eliminarlo para mantener consistencia
            if archivo_guardado and os.path.exists(archivo_guardado):
                try:
                    os.remove(archivo_guardado)
                    print(f"✗ Archivo eliminado por error: {archivo_guardado}")
                except:
                    pass
            print(f"✗ Error al guardar resultado: {str(e)}")
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('main.admin_resultados'))
    
    resultados = Resultado.query.order_by(Resultado.fecha_creacion.desc()).all()
    pacientes = Paciente.query.order_by(Paciente.nombre).all()
    return render_template('admin/resultados.html', resultados=resultados, pacientes=pacientes)

@main.route('/descargar-credenciales-pdf/<int:resultado_id>')
@admin_required
def descargar_credenciales_pdf(resultado_id):
    resultado = Resultado.query.get_or_404(resultado_id)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Logo (si existe)
    try:
        logo = Image('app/static/img/logo.jpg', width=1.5*inch, height=1.5*inch)
        elements.append(logo)
    except:
        pass
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Título
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1ABC9C'),
        spaceAfter=20,
        alignment=1
    )
    elements.append(Paragraph('LABORATORIO CLÍNICO PÉREZ', title_style))
    elements.append(Paragraph('Potosí, Bolivia', styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Tabla de credenciales
    data = [
        ['CREDENCIALES DE ACCESO A RESULTADOS'],
        [''],
        ['INFORMACIÓN DEL PACIENTE'],
        ['Nombre Completo:', resultado.paciente_nombre],
        ['Cédula de Identidad:', resultado.paciente_ci],
        ['Número de Orden:', resultado.numero_orden],
        [''],
        ['CREDENCIALES DE ACCESO'],
        ['CI:', resultado.paciente_ci],
        ['CÓDIGO DE ACCESO:', resultado.codigo_acceso],
        [''],
        ['INSTRUCCIONES'],
        ['1. Ingrese a: http://localhost:5000', ''],
        ['2. Click en "Ver mis Resultados"', ''],
        ['3. Ingrese su CI y código de acceso', ''],
        ['4. Descargue su resultado en PDF', ''],
        [''],
        [f'Fecha de Emisión: {resultado.fecha_creacion.strftime("%d/%m/%Y %H:%M")}', '']
    ]
    
    table = Table(data, colWidths=[2.5*inch, 3.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1ABC9C')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#F39C12')),
        ('TEXTCOLOR', (0, 2), (-1, 2), colors.whitesmoke),
        ('BACKGROUND', (0, 7), (-1, 7), colors.HexColor('#F39C12')),
        ('TEXTCOLOR', (0, 7), (-1, 7), colors.whitesmoke),
        ('BACKGROUND', (0, 11), (-1, 11), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 11), (-1, 11), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    filename = f"Credenciales_{resultado.paciente_nombre.replace(' ', '_')}.pdf"
    
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

@main.route('/descargar-credenciales-word/<int:resultado_id>')
@admin_required
def descargar_credenciales_word(resultado_id):
    resultado = Resultado.query.get_or_404(resultado_id)
    
    doc = Document()
    
    # Logo
    try:
        doc.add_picture('app/static/img/logo.jpg', width=Inches(1.5))
    except:
        pass
    
    # Título
    titulo = doc.add_heading('LABORATORIO CLÍNICO PÉREZ', 0)
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    titulo.runs[0].font.color.rgb = RGBColor(26, 188, 156)
    
    subtitulo = doc.add_paragraph('Potosí, Bolivia')
    subtitulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()
    
    # Tabla de credenciales
    table = doc.add_table(rows=13, cols=2)
    table.style = 'Light Grid Accent 1'
    
    # Encabezado
    header_cell = table.rows[0].cells[0]
    header_cell.merge(table.rows[0].cells[1])
    header_cell.text = 'CREDENCIALES DE ACCESO A RESULTADOS'
    header_cell.paragraphs[0].runs[0].font.bold = True
    header_cell.paragraphs[0].runs[0].font.size = Pt(14)
    header_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Información del paciente
    table.rows[1].cells[0].merge(table.rows[1].cells[1])
    table.rows[1].cells[0].text = 'INFORMACIÓN DEL PACIENTE'
    table.rows[1].cells[0].paragraphs[0].runs[0].font.bold = True
    
    table.rows[2].cells[0].text = 'Nombre Completo:'
    table.rows[2].cells[1].text = resultado.paciente_nombre
    
    table.rows[3].cells[0].text = 'Cédula de Identidad:'
    table.rows[3].cells[1].text = resultado.paciente_ci
    
    table.rows[4].cells[0].text = 'Número de Orden:'
    table.rows[4].cells[1].text = resultado.numero_orden
    
    # Credenciales
    table.rows[5].cells[0].merge(table.rows[5].cells[1])
    table.rows[5].cells[0].text = 'CREDENCIALES DE ACCESO'
    table.rows[5].cells[0].paragraphs[0].runs[0].font.bold = True
    
    table.rows[6].cells[0].text = 'CI:'
    table.rows[6].cells[1].text = resultado.paciente_ci
    
    table.rows[7].cells[0].text = 'CÓDIGO DE ACCESO:'
    table.rows[7].cells[1].text = resultado.codigo_acceso
    table.rows[7].cells[1].paragraphs[0].runs[0].font.bold = True
    table.rows[7].cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(231, 76, 60)
    
    # Instrucciones
    table.rows[8].cells[0].merge(table.rows[8].cells[1])
    table.rows[8].cells[0].text = 'INSTRUCCIONES'
    table.rows[8].cells[0].paragraphs[0].runs[0].font.bold = True
    
    table.rows[9].cells[0].merge(table.rows[9].cells[1])
    table.rows[9].cells[0].text = '1. Ingrese a: http://localhost:5000'
    
    table.rows[10].cells[0].merge(table.rows[10].cells[1])
    table.rows[10].cells[0].text = '2. Click en "Ver mis Resultados"'
    
    table.rows[11].cells[0].merge(table.rows[11].cells[1])
    table.rows[11].cells[0].text = '3. Ingrese su CI y código de acceso'
    
    table.rows[12].cells[0].merge(table.rows[12].cells[1])
    table.rows[12].cells[0].text = f'Fecha de Emisión: {resultado.fecha_creacion.strftime("%d/%m/%Y %H:%M")}'
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    filename = f"Credenciales_{resultado.paciente_nombre.replace(' ', '_')}.docx"
    
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

@main.route('/pruebas', methods=['GET', 'POST'])
@admin_required
def admin_pruebas():
    if request.method == 'POST':
        try:
            # Manejar imagen si se subió
            imagen_filename = None
            if 'imagen' in request.files:
                imagen = request.files['imagen']
                if imagen and imagen.filename:
                    # Crear carpeta si no existe
                    os.makedirs(PRUEBAS_UPLOAD_DIR, exist_ok=True)

                    # Guardar imagen con nombre seguro
                    from werkzeug.utils import secure_filename
                    import time
                    filename = secure_filename(imagen.filename)
                    imagen_filename = f"{int(time.time())}_{filename}"
                    imagen.save(os.path.join(PRUEBAS_UPLOAD_DIR, imagen_filename))

            prueba = Prueba(
                nombre=request.form['nombre'],
                categoria=request.form.get('categoria'),
                descripcion=request.form.get('descripcion'),
                precio=float(request.form.get('precio', 0)),
                imagen=imagen_filename
            )
            db.session.add(prueba)
            db.session.commit()
            flash('Prueba registrada exitosamente', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('main.admin_pruebas'))

    pruebas = Prueba.query.order_by(Prueba.nombre).all()

    # Obtener categorías únicas de la base de datos
    categorias = db.session.query(Prueba.categoria).distinct().filter(Prueba.categoria.isnot(None)).order_by(Prueba.categoria).all()
    categorias_list = [cat[0] for cat in categorias if cat[0]]

    return render_template('admin/pruebas.html', pruebas=pruebas, categorias=categorias_list)

@main.route('/prueba/<int:prueba_id>')
@admin_required
def ver_prueba(prueba_id):
    prueba = Prueba.query.get_or_404(prueba_id)
    return jsonify({
        'id': prueba.id,
        'nombre': prueba.nombre,
        'categoria': prueba.categoria,
        'descripcion': prueba.descripcion,
        'precio': float(prueba.precio),
        'imagen': prueba.imagen
    })

@main.route('/prueba/editar/<int:prueba_id>', methods=['POST'])
@admin_required
def editar_prueba(prueba_id):
    try:
        prueba = Prueba.query.get_or_404(prueba_id)
        prueba.nombre = request.form['nombre']
        prueba.categoria = request.form.get('categoria')
        prueba.descripcion = request.form.get('descripcion')
        prueba.precio = float(request.form.get('precio', 0))

        # Manejar nueva imagen si se subió
        if 'imagen' in request.files:
            imagen = request.files['imagen']
            if imagen and imagen.filename:
                # Eliminar imagen anterior si existe
                if prueba.imagen:
                    old_path = os.path.join(PRUEBAS_UPLOAD_DIR, prueba.imagen)
                    if os.path.exists(old_path):
                        os.remove(old_path)

                # Guardar nueva imagen
                from werkzeug.utils import secure_filename
                import time
                filename = secure_filename(imagen.filename)
                imagen_filename = f"{int(time.time())}_{filename}"
                os.makedirs(PRUEBAS_UPLOAD_DIR, exist_ok=True)
                imagen.save(os.path.join(PRUEBAS_UPLOAD_DIR, imagen_filename))
                prueba.imagen = imagen_filename

        db.session.commit()
        flash('Prueba actualizada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('main.admin_pruebas'))

@main.route('/prueba/eliminar/<int:prueba_id>', methods=['POST'])
@admin_required
def eliminar_prueba(prueba_id):
    try:
        prueba = Prueba.query.get_or_404(prueba_id)
        nombre_prueba = prueba.nombre

        # Eliminar imagen si existe
        if prueba.imagen:
            try:
                imagen_path = os.path.join(PRUEBAS_UPLOAD_DIR, prueba.imagen)
                if os.path.exists(imagen_path):
                    os.remove(imagen_path)
            except Exception as e:
                print(f"Error eliminando imagen {prueba.imagen}: {e}")

        db.session.delete(prueba)
        db.session.commit()
        flash(f'Prueba "{nombre_prueba}" eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar prueba: {str(e)}', 'danger')
    return redirect(url_for('main.admin_pruebas'))

@main.route('/descargar/<int:resultado_id>')
@admin_required
def descargar(resultado_id):
    resultado = Resultado.query.get_or_404(resultado_id)
    if resultado.archivo_pdf:
        # Construir ruta absoluta correcta usando UPLOAD_DIR
        pdf_path = os.path.join(UPLOAD_DIR, resultado.archivo_pdf)

        # Verificar que el archivo existe
        if not os.path.exists(pdf_path):
            flash(f'El archivo PDF no se encuentra en el servidor: {resultado.archivo_pdf}', 'danger')
            return redirect(url_for('main.admin_resultados'))

        return send_file(pdf_path, as_attachment=True)

    flash('No hay archivo PDF disponible', 'warning')
    return redirect(url_for('main.admin_resultados'))













