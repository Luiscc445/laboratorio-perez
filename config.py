import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'lab_perez_default_key')

    # Usar Supabase PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    # Reemplazar postgres:// con postgresql:// si es necesario (Heroku/Render fix)
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ============ CONFIGURACIÓN OPTIMIZADA PARA RENDER ============
    # Connection pooling optimizado para evitar "Connection refused"
    SQLALCHEMY_ENGINE_OPTIONS = {
        # Pool de conexiones
        'pool_size': 5,              # Máximo 5 conexiones simultáneas (Render free tier)
        'pool_recycle': 280,         # Reciclar conexiones cada 280s (antes de 5min timeout)
        'pool_pre_ping': True,       # Verificar conexión antes de usar (evita errores)
        'max_overflow': 2,           # Máximo 2 conexiones extra si pool está lleno

        # Timeouts y reconexión automática
        'connect_args': {
            'connect_timeout': 10,   # Timeout de conexión: 10 segundos
            'keepalives': 1,         # Mantener conexión viva
            'keepalives_idle': 30,   # Enviar keepalive cada 30s
            'keepalives_interval': 10,  # Intervalo entre keepalives
            'keepalives_count': 5,   # Máximo 5 intentos de keepalive
        },

        # Reintentos automáticos si falla la conexión
        'echo_pool': False,          # No hacer logging del pool (menos ruido)
        'pool_timeout': 30,          # Timeout esperando conexión del pool
    }

    # Supabase configuración
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

    # Configuración de archivos
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
