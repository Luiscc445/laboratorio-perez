from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    ci = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    resultados = db.relationship('Resultado', backref='paciente', lazy=True, cascade='all, delete-orphan')

class Resultado(db.Model):
    __tablename__ = 'resultados'
    id = db.Column(db.Integer, primary_key=True)
    numero_orden = db.Column(db.String(50), unique=True, nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=True)
    paciente_nombre = db.Column(db.String(200), nullable=False)
    paciente_ci = db.Column(db.String(20), nullable=False)
    fecha_muestra = db.Column(db.Date)
    archivo_pdf = db.Column(db.String(200))
    codigo_acceso = db.Column(db.String(20))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Prueba(db.Model):
    __tablename__ = 'pruebas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100))
    precio = db.Column(db.Float, default=0.0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
