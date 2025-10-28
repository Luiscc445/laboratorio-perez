from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Paciente
from app import db

pacientes_bp = Blueprint('pacientes', __name__, url_prefix='/pacientes')

@pacientes_bp.route('/')
@login_required
def listar():
    pacientes = Paciente.query.order_by(Paciente.fecha_registro.desc()).all()
    return render_template('pacientes/listar.html', pacientes=pacientes)

@pacientes_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear_paciente():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        ci = request.form.get('ci')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        
        # Verificar si el CI ya existe ANTES
        paciente_existente = Paciente.query.filter_by(ci=ci).first()
        if paciente_existente:
            flash('⚠️ Ya existe un paciente con ese CI', 'warning')
            return redirect(url_for('pacientes.listar'))
        
        nuevo_paciente = Paciente(
            nombre=nombre,
            ci=ci,
            telefono=telefono,
            email=email
        )
        
        try:
            db.session.add(nuevo_paciente)
            db.session.commit()
            flash('✅ Paciente registrado exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash('❌ Error al registrar paciente', 'danger')
        
        return redirect(url_for('pacientes.listar'))
    
    return render_template('pacientes/crear.html')

@pacientes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    paciente = Paciente.query.get_or_404(id)
    
    if request.method == 'POST':
        ci_nuevo = request.form.get('ci')
        
        if ci_nuevo != paciente.ci:
            paciente_existente = Paciente.query.filter_by(ci=ci_nuevo).first()
            if paciente_existente:
                flash('⚠️ Ya existe otro paciente con ese CI', 'warning')
                return redirect(url_for('pacientes.editar', id=id))
        
        paciente.nombre = request.form.get('nombre')
        paciente.ci = ci_nuevo
        paciente.telefono = request.form.get('telefono')
        paciente.email = request.form.get('email')
        
        try:
            db.session.commit()
            flash('✅ Paciente actualizado exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash('❌ Error al actualizar paciente', 'danger')
        
        return redirect(url_for('pacientes.listar'))
    
    return render_template('pacientes/editar.html', paciente=paciente)

@pacientes_bp.route('/ver/<int:id>')
@login_required
def ver(id):
    paciente = Paciente.query.get_or_404(id)
    return render_template('pacientes/ver.html', paciente=paciente)
