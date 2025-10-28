from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import Usuario

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and usuario.check_password(password):
            login_user(usuario)
            return redirect(url_for('main.dashboard'))
        flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
