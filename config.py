import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'lab_perez_default_key')
    
    # Usar Supabase PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # Reemplazar postgres:// con postgresql:// si es necesario (Heroku fix)
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Supabase configuración
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Configuración de archivos
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
