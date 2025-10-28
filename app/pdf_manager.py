import os
import secrets
from pathlib import Path
from datetime import datetime
from werkzeug.utils import secure_filename

class PDFManager:
    def __init__(self, upload_folder):
        self.upload_folder = Path(upload_folder)
        self.upload_folder.mkdir(parents=True, exist_ok=True)
    
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'
    
    def generate_filename(self, numero_orden, original_filename):
        safe_name = secure_filename(original_filename)
        name_without_ext = safe_name.rsplit('.', 1)[0] if '.' in safe_name else safe_name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = secrets.token_hex(4)
        return f"{numero_orden}_{name_without_ext}_{timestamp}_{unique_id}.pdf"
    
    def save_pdf(self, file, numero_orden):
        if not file or file.filename == '':
            return False, None, "No se seleccionó ningún archivo"
        if not self.allowed_file(file.filename):
            return False, None, "El archivo debe ser PDF"
        try:
            filename = self.generate_filename(numero_orden, file.filename)
            filepath = self.upload_folder / filename
            file.save(str(filepath))
            relative_path = f"app/uploads/resultados/{filename}"
            return True, relative_path, None
        except Exception as e:
            return False, None, f"Error al guardar: {str(e)}"
    
    def get_full_path(self, relative_path):
        if not relative_path:
            return None
        path = Path(relative_path)
        if path.is_absolute() and path.exists():
            return path
        base_dir = Path(__file__).parent.parent.absolute()
        full_path = base_dir / relative_path
        return full_path if full_path.exists() else None
    
    def delete_pdf(self, relative_path):
        try:
            full_path = self.get_full_path(relative_path)
            if full_path and full_path.exists():
                full_path.unlink()
                return True
            return False
        except:
            return False
