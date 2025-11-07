from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os
from sqlalchemy.exc import OperationalError, TimeoutError, DBAPIError

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes import main
    from app.auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # NOTA: db.create_all() comentado para evitar WORKER TIMEOUT en Render
    # Las tablas ya están creadas en Supabase, no es necesario crearlas cada vez
    # with app.app_context():
    #     db.create_all()

    # ============ MANEJO DE ERRORES PARA RENDER ============

    @app.errorhandler(OperationalError)
    def handle_db_connection_error(e):
        """Maneja errores de conexión a la base de datos"""
        app.logger.error(f'Error de conexión a BD: {str(e)}')
        return render_template_string('''
            <!DOCTYPE html>
            <html><head><title>Error de Conexión</title>
            <style>
                body { font-family: Arial; text-align: center; padding: 50px; background: #f5f5f5; }
                .error-box { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }
                h1 { color: #e74c3c; }
                p { color: #666; line-height: 1.6; }
                .btn { background: #1ABC9C; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
            </style></head><body>
                <div class="error-box">
                    <h1>⚠️ Estamos Trabajando en Ello</h1>
                    <p>Temporalmente no podemos conectarnos a la base de datos.</p>
                    <p>Por favor, intenta nuevamente en unos segundos.</p>
                    <a href="/" class="btn">← Volver al Inicio</a>
                </div>
            </body></html>
        '''), 503

    @app.errorhandler(500)
    def handle_internal_error(e):
        """Maneja errores internos del servidor"""
        app.logger.error(f'Error 500: {str(e)}')
        return render_template_string('''
            <!DOCTYPE html>
            <html><head><title>Error Interno</title>
            <style>
                body { font-family: Arial; text-align: center; padding: 50px; background: #f5f5f5; }
                .error-box { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }
                h1 { color: #e74c3c; }
                p { color: #666; line-height: 1.6; }
                .btn { background: #1ABC9C; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
            </style></head><body>
                <div class="error-box">
                    <h1>😔 Algo Salió Mal</h1>
                    <p>Estamos trabajando para resolver el problema.</p>
                    <a href="/" class="btn">← Volver al Inicio</a>
                </div>
            </body></html>
        '''), 500

    @app.errorhandler(404)
    def handle_not_found(e):
        """Maneja páginas no encontradas"""
        return render_template_string('''
            <!DOCTYPE html>
            <html><head><title>Página No Encontrada</title>
            <style>
                body { font-family: Arial; text-align: center; padding: 50px; background: #f5f5f5; }
                .error-box { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }
                h1 { color: #3498DB; }
                p { color: #666; line-height: 1.6; }
                .btn { background: #1ABC9C; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
            </style></head><body>
                <div class="error-box">
                    <h1>🔍 404 - Página No Encontrada</h1>
                    <p>La página que buscas no existe.</p>
                    <a href="/" class="btn">← Volver al Inicio</a>
                </div>
            </body></html>
        '''), 404

    return app

def render_template_string(html_string):
    """Helper para renderizar HTML inline"""
    from flask import Response
    return Response(html_string, mimetype='text/html')
