#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para arreglar la base de datos automáticamente
Ejecutar: python arreglar_base_datos.py
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from sqlalchemy import text

def arreglar_base_datos():
    """Elimina restricción UNIQUE de numero_orden y agrega a codigo_acceso"""

    print("=" * 80)
    print("🔧 ARREGLANDO BASE DE DATOS - LABORATORIO PÉREZ")
    print("=" * 80)
    print()

    app = create_app()

    with app.app_context():
        try:
            # ============ PASO 1: Verificar conexión ============
            print("📡 Verificando conexión a la base de datos...")
            result = db.session.execute(text("SELECT current_database();"))
            db_name = result.fetchone()[0]
            print(f"✅ Conectado a: {db_name}")
            print()

            # ============ PASO 2: Verificar restricción actual ============
            print("🔍 Buscando restricción UNIQUE en numero_orden...")
            result = db.session.execute(text("""
                SELECT constraint_name
                FROM information_schema.table_constraints
                WHERE table_name = 'resultados'
                AND constraint_type = 'UNIQUE'
                AND constraint_name LIKE '%numero_orden%';
            """))

            constraints = result.fetchall()

            if constraints:
                constraint_name = constraints[0][0]
                print(f"❌ Encontrada restricción problemática: {constraint_name}")
                print(f"   Esta restricción impide subir múltiples resultados.")
                print()

                # ============ PASO 3: Eliminar restricción ============
                print(f"🗑️  Eliminando restricción '{constraint_name}'...")
                db.session.execute(text(f"""
                    ALTER TABLE resultados
                    DROP CONSTRAINT IF EXISTS {constraint_name};
                """))
                db.session.commit()
                print(f"✅ Restricción '{constraint_name}' eliminada exitosamente!")
                print()
            else:
                print("✅ No se encontró restricción UNIQUE en numero_orden")
                print("   (Ya está correcto)")
                print()

            # ============ PASO 4: Agregar restricción a codigo_acceso ============
            print("🔍 Verificando restricción UNIQUE en codigo_acceso...")
            result = db.session.execute(text("""
                SELECT constraint_name
                FROM information_schema.table_constraints
                WHERE table_name = 'resultados'
                AND constraint_type = 'UNIQUE'
                AND constraint_name LIKE '%codigo_acceso%';
            """))

            codigo_constraints = result.fetchall()

            if not codigo_constraints:
                print("➕ Agregando restricción UNIQUE a codigo_acceso...")
                try:
                    db.session.execute(text("""
                        ALTER TABLE resultados
                        ADD CONSTRAINT resultados_codigo_acceso_unique
                        UNIQUE (codigo_acceso);
                    """))
                    db.session.commit()
                    print("✅ Restricción UNIQUE agregada a codigo_acceso!")
                    print()
                except Exception as e:
                    if 'already exists' in str(e).lower():
                        print("✅ Restricción ya existe (correcto)")
                        print()
                    else:
                        raise
            else:
                print("✅ codigo_acceso ya tiene restricción UNIQUE (correcto)")
                print()

            # ============ PASO 5: Verificar estado final ============
            print("📊 Estado final de la tabla 'resultados':")
            print("-" * 80)

            result = db.session.execute(text("""
                SELECT
                    tc.constraint_name,
                    tc.constraint_type,
                    kcu.column_name
                FROM information_schema.table_constraints tc
                LEFT JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                WHERE tc.table_name = 'resultados'
                ORDER BY tc.constraint_type, tc.constraint_name;
            """))

            constraints_found = False
            for row in result:
                constraints_found = True
                constraint_name, constraint_type, column_name = row
                print(f"   {constraint_type:15s} | {column_name or 'N/A':20s} | {constraint_name}")

            if not constraints_found:
                print("   (No se encontraron restricciones)")

            print("-" * 80)
            print()

            # ============ PASO 6: Crear carpetas necesarias ============
            print("📁 Creando carpetas para PDFs...")

            uploads_dir = os.path.join('app', 'static', 'uploads')
            backups_dir = os.path.join(uploads_dir, 'backups')
            pruebas_dir = os.path.join(uploads_dir, 'pruebas')

            os.makedirs(uploads_dir, exist_ok=True)
            os.makedirs(backups_dir, exist_ok=True)
            os.makedirs(pruebas_dir, exist_ok=True)

            print(f"✅ {uploads_dir}/")
            print(f"✅ {backups_dir}/")
            print(f"✅ {pruebas_dir}/")
            print()

            # ============ ÉXITO ============
            print("=" * 80)
            print("🎉 BASE DE DATOS ARREGLADA EXITOSAMENTE")
            print("=" * 80)
            print()
            print("✅ CAMBIOS REALIZADOS:")
            print("   • Restricción UNIQUE eliminada de 'numero_orden'")
            print("   • Restricción UNIQUE agregada a 'codigo_acceso'")
            print("   • Carpetas de uploads creadas correctamente")
            print()
            print("🚀 AHORA PUEDES:")
            print("   • Subir múltiples resultados al mismo paciente")
            print("   • El sistema generará números de orden automáticos")
            print("   • Cada PDF se guarda con backup automático")
            print("   • Nunca se perderán archivos")
            print()
            print("📝 PRÓXIMO PASO:")
            print("   1. Reinicia Flask (Ctrl+C y vuelve a ejecutar)")
            print("   2. Ve a: http://127.0.0.1:5000/resultados")
            print("   3. Sube un nuevo resultado (deja número de orden vacío)")
            print("   4. ¡Disfruta del sistema robusto!")
            print()
            print("=" * 80)

            return True

        except Exception as e:
            print()
            print("=" * 80)
            print("❌ ERROR AL ARREGLAR BASE DE DATOS")
            print("=" * 80)
            print()
            print(f"Error: {str(e)}")
            print()
            print("Posibles soluciones:")
            print("1. Verifica que la base de datos esté accesible")
            print("2. Verifica las credenciales en .env")
            print("3. Verifica que tengas permisos para modificar la tabla")
            print()
            return False

if __name__ == "__main__":
    try:
        success = arreglar_base_datos()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
