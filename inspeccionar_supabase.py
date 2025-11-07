#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para inspeccionar estructura de Supabase
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Prueba

def main():
    print("=" * 70)
    print("🔍 INSPECCIÓN DE SUPABASE")
    print("=" * 70)

    app = create_app()

    with app.app_context():
        try:
            # Obtener info de la tabla
            inspector = db.inspect(db.engine)

            print("\n📋 TABLAS EN LA BASE DE DATOS:")
            print("-" * 70)
            tablas = inspector.get_table_names()
            for tabla in tablas:
                print(f"   ✅ {tabla}")

            # Estructura de la tabla pruebas
            if 'pruebas' in tablas:
                print("\n📊 ESTRUCTURA DE 'pruebas':")
                print("-" * 70)
                columnas = inspector.get_columns('pruebas')

                print(f"   {'Columna':<20} {'Tipo':<25} {'Null':<8}")
                print("   " + "-" * 55)
                for col in columnas:
                    nombre = col['name']
                    tipo = str(col['type'])
                    nullable = "SI" if col['nullable'] else "NO"
                    print(f"   {nombre:<20} {tipo:<25} {nullable:<8}")

                # Contar registros
                count = Prueba.query.count()
                print(f"\n   📊 Total de registros: {count}")

                if count > 0:
                    # Mostrar primeros 3
                    print(f"\n   📝 Primeros 3 registros:")
                    pruebas = Prueba.query.limit(3).all()
                    for i, p in enumerate(pruebas, 1):
                        print(f"      {i}. ID: {p.id} | {p.nombre} | {p.categoria} | ${p.precio}")

                    # Buscar ORINA
                    print(f"\n   🔍 Buscando examen de ORINA...")
                    orina = Prueba.query.filter(
                        Prueba.nombre.ilike('%ORINA%')
                    ).first()

                    if orina:
                        print(f"      ✅ Encontrado:")
                        print(f"         ID: {orina.id}")
                        print(f"         Nombre: {orina.nombre}")
                        print(f"         Categoría: {orina.categoria}")
                        print(f"         Precio: ${orina.precio}")
                        if hasattr(orina, 'imagen'):
                            print(f"         Imagen: {orina.imagen}")
                        else:
                            print(f"         ⚠️  NO tiene columna 'imagen'")
                    else:
                        print(f"      ❌ No se encontró examen de ORINA")

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("✅ INSPECCIÓN COMPLETADA")
    print("=" * 70)

if __name__ == "__main__":
    main()
