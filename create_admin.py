#!/usr/bin/env python3
"""
Script para crear el usuario administrador del sistema
Laboratorio Pérez - Sistema de Gestión con Supabase
"""

from app import create_app, db
from app.models import Usuario

def create_admin_user():
    """Crea el usuario administrador con credenciales seguras en Supabase"""
    app = create_app()

    with app.app_context():
        # Credenciales del administrador
        username = 'DoctorMauricoPerezPTS574'
        password = 'Cachuchin574'

        print("\n" + "=" * 70)
        print("🔒 SISTEMA DE SEGURIDAD - LABORATORIO PÉREZ")
        print("=" * 70)
        print("\n🔍 PASO 1: Verificando usuarios existentes en Supabase...\n")

        # Eliminar TODOS los usuarios antiguos
        usuarios_antiguos = Usuario.query.all()
        if usuarios_antiguos:
            print(f"⚠️  Encontrados {len(usuarios_antiguos)} usuario(s) antiguo(s):")
            for u in usuarios_antiguos:
                print(f"   - ID: {u.id}, Username: {u.username}, Admin: {u.is_admin}")

            print("\n🗑️  Eliminando usuarios antiguos de Supabase...")
            for u in usuarios_antiguos:
                db.session.delete(u)
            db.session.commit()
            print("✅ Usuarios antiguos eliminados correctamente\n")
        else:
            print("✅ No hay usuarios antiguos. Base de datos limpia.\n")

        print("🔧 PASO 2: Creando nuevo usuario administrador...\n")

        # Crear nuevo usuario administrador
        admin = Usuario(
            username=username,
            is_admin=True
        )
        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()

        # Verificar que se creó correctamente
        verificacion = Usuario.query.filter_by(username=username).first()

        print("=" * 70)
        print("✅ USUARIO ADMINISTRADOR CREADO EXITOSAMENTE EN SUPABASE")
        print("=" * 70)
        print(f"\n📋 DATOS DEL ADMINISTRADOR:")
        print(f"   • ID en Supabase: {verificacion.id}")
        print(f"   • Usuario: {username}")
        print(f"   • Contraseña: {password}")
        print(f"   • Rol: Administrador (is_admin=True)")
        print(f"   • Hash en BD: {verificacion.password_hash[:50]}...")
        print(f"   • Fecha creación: {verificacion.fecha_creacion}")
        print("\n" + "=" * 70)
        print("🔒 INFORMACIÓN DE SEGURIDAD:")
        print("=" * 70)
        print("   ✓ Contraseña hasheada con Werkzeug (pbkdf2:sha256)")
        print("   ✓ Solo este usuario puede acceder al sistema administrativo")
        print("   ✓ Todas las rutas admin protegidas con @admin_required")
        print("   ✓ Hash almacenado de forma segura en Supabase")
        print("\n" + "=" * 70)
        print("🌐 ACCESO AL SISTEMA:")
        print("=" * 70)
        print(f"   URL: http://localhost:5000/auth/login")
        print(f"   Usuario: {username}")
        print(f"   Contraseña: {password}")
        print("\n" + "=" * 70)
        print("⚠️  GUARDA ESTAS CREDENCIALES EN UN LUGAR SEGURO")
        print("=" * 70 + "\n")

if __name__ == '__main__':
    create_admin_user()
