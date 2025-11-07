#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para renumerar los IDs de las pruebas de 1 a 167 en Supabase
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Prueba

def renumerar_ids():
    print("=" * 70)
    print("🔢 RENUMERACIÓN DE IDs DE PRUEBAS - SUPABASE")
    print("=" * 70)

    app = create_app()

    with app.app_context():
        try:
            # Obtener todas las pruebas ordenadas por ID actual
            pruebas = Prueba.query.order_by(Prueba.id).all()
            total = len(pruebas)

            print(f"\n📊 Total de pruebas encontradas: {total}")

            if total == 0:
                print("❌ No hay pruebas en la base de datos")
                return

            # Mostrar rango actual de IDs
            primer_id = pruebas[0].id
            ultimo_id = pruebas[-1].id

            print(f"📍 Rango actual de IDs: {primer_id} → {ultimo_id}")
            print(f"🎯 Nuevo rango de IDs: 1 → {total}")

            # Confirmación
            print(f"\n⚠️  ADVERTENCIA: Esta operación renumerará todos los IDs")
            print(f"   - Se eliminarán los IDs actuales ({primer_id}-{ultimo_id})")
            print(f"   - Se crearán nuevos IDs secuenciales (1-{total})")
            confirmacion = input("\n¿Continuar? (SI/NO): ")

            if confirmacion.upper() != "SI":
                print("❌ Operación cancelada")
                return

            print("\n⚡ Iniciando renumeración...")
            print("-" * 70)

            # Estrategia: Guardar datos, eliminar todas, recrear con nuevos IDs
            print("📋 Paso 1: Guardando datos de las pruebas...")

            datos_pruebas = []
            for prueba in pruebas:
                datos_pruebas.append({
                    'nombre': prueba.nombre,
                    'categoria': prueba.categoria,
                    'descripcion': prueba.descripcion if hasattr(prueba, 'descripcion') else None,
                    'precio': prueba.precio,
                    'imagen': prueba.imagen,
                    'fecha_creacion': prueba.fecha_creacion
                })

            print(f"   ✅ {len(datos_pruebas)} pruebas guardadas en memoria")

            # Eliminar todas las pruebas
            print("\n🗑️  Paso 2: Eliminando pruebas actuales...")
            Prueba.query.delete()
            db.session.commit()
            print("   ✅ Todas las pruebas eliminadas")

            # Resetear el contador de secuencia en PostgreSQL
            print("\n🔄 Paso 3: Reseteando secuencia de IDs...")
            try:
                # En PostgreSQL, resetear la secuencia
                db.session.execute(db.text("ALTER SEQUENCE pruebas_id_seq RESTART WITH 1"))
                db.session.commit()
                print("   ✅ Secuencia reseteada a 1")
            except Exception as e:
                print(f"   ⚠️  No se pudo resetear secuencia (puede ser normal): {str(e)}")

            # Recrear las pruebas con nuevos IDs
            print("\n➕ Paso 4: Recreando pruebas con IDs nuevos (1-{})...".format(len(datos_pruebas)))

            contador = 0
            for datos in datos_pruebas:
                nueva_prueba = Prueba(
                    nombre=datos['nombre'],
                    categoria=datos['categoria'],
                    descripcion=datos.get('descripcion'),
                    precio=datos['precio'],
                    imagen=datos['imagen'],
                    fecha_creacion=datos['fecha_creacion']
                )
                db.session.add(nueva_prueba)
                contador += 1

                # Commit cada 50 pruebas
                if contador % 50 == 0:
                    db.session.commit()
                    print(f"   ✅ {contador} pruebas recreadas...")

            # Commit final
            db.session.commit()
            print(f"   ✅ {contador} pruebas recreadas completamente")

            # Verificar resultado
            print("\n🔍 Paso 5: Verificando resultado...")
            pruebas_finales = Prueba.query.order_by(Prueba.id).all()

            if pruebas_finales:
                primer_id_nuevo = pruebas_finales[0].id
                ultimo_id_nuevo = pruebas_finales[-1].id
                total_final = len(pruebas_finales)

                print(f"   ✅ Total de pruebas: {total_final}")
                print(f"   ✅ Rango de IDs: {primer_id_nuevo} → {ultimo_id_nuevo}")

                # Mostrar primeras 5 pruebas
                print("\n📝 Primeras 5 pruebas con nuevos IDs:")
                for i, p in enumerate(pruebas_finales[:5], 1):
                    print(f"   {i}. ID: {p.id} - {p.nombre} ({p.categoria})")

                # Mostrar últimas 3 pruebas
                print("\n📝 Últimas 3 pruebas:")
                for p in pruebas_finales[-3:]:
                    print(f"   {len(pruebas_finales) - pruebas_finales.index(p)}. ID: {p.id} - {p.nombre} ({p.categoria})")

            else:
                print("   ❌ No se encontraron pruebas después de la operación")

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            return

    print("\n" + "=" * 70)
    print("✅ RENUMERACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print("\n💡 Los IDs ahora van del 1 al {}".format(total))
    print("💡 Puedes verificar en el panel admin: /admin/pruebas")

if __name__ == "__main__":
    renumerar_ids()
