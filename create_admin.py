#!/usr/bin/env python3
"""
Script para crear el usuario administrador del sistema
Laboratorio Pérez - Sistema de Gestión
"""

from app import create_app, db
from app.models import Usuario

def create_admin_user():
    """Crea el usuario administrador con credenciales seguras"""
    app = create_app()

    with app.app_context():
        # Verificar si ya existe el usuario
        username = 'DoctorMauricoPerezPTS574'
        existing_user = Usuario.query.filter_by(username=username).first()

        if existing_user:
            print(f"⚠️  El usuario '{username}' ya existe.")
            respuesta = input("¿Deseas actualizar su contraseña? (s/n): ")
            if respuesta.lower() != 's':
                print("❌ Operación cancelada.")
                return

            # Actualizar contraseña
            existing_user.set_password('Cachuchin574')
            existing_user.is_admin = True
            db.session.commit()
            print(f"✅ Contraseña actualizada para '{username}'")
        else:
            # Crear nuevo usuario administrador
            admin = Usuario(
                username=username,
                is_admin=True
            )
            admin.set_password('Cachuchin574')

            db.session.add(admin)
            db.session.commit()

            print("=" * 60)
            print("✅ USUARIO ADMINISTRADOR CREADO EXITOSAMENTE")
            print("=" * 60)
            print(f"Usuario: {username}")
            print(f"Contraseña: Cachuchin574 (hasheada con Werkzeug)")
            print(f"Rol: Administrador (is_admin=True)")
            print(f"ID: {admin.id}")
            print("=" * 60)
            print("\n🔒 IMPORTANTE:")
            print("1. La contraseña está hasheada en la base de datos")
            print("2. Solo este usuario puede acceder al panel administrativo")
            print("3. Guarda estas credenciales en un lugar seguro")
            print(f"4. URL de acceso: http://localhost:5000/auth/login")
            print("=" * 60)

if __name__ == '__main__':
    create_admin_user()
