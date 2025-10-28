import os
from pathlib import Path

class Config:
    # Base directory
    BASE_DIR = Path(__file__).parent.absolute()
    
    # Upload configuration
    UPLOAD_FOLDER = BASE_DIR / 'app' / 'uploads' / 'resultados'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Ensure upload folder exists
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret key
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
