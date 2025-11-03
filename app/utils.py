"""
Utilidades de seguridad - Laboratorio Pérez
"""
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """
    Decorador para requerir que el usuario esté autenticado Y sea administrador.
    Uso: @admin_required en lugar de solo @login_required para rutas administrativas.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Por favor inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            flash('No tienes permisos para acceder a esta página.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function
