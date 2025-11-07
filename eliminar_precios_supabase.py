#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 SCRIPT RÁPIDO: Eliminar TODOS los precios en Supabase
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Prueba

def main():
    print("=" * 70)
    print("⚡ ELIMINAR PRECIOS - SUPABASE")
    print("=" * 70)

    app = create_app()

    with app.app_context():
        try:
            # Contar
            total = Prueba.query.count()
            con_precio = Prueba.query.filter(Prueba.precio > 0).count()

            print(f"\n📊 Total de pruebas: {total}")
            print(f"💵 Pruebas con precio > 0: {con_precio}")

            if con_precio == 0:
                print("\n✅ Todos los precios ya están en 0.00")
                return

            # Mostrar ejemplos
            print(f"\n📝 Ejemplos de pruebas con precio:")
            ejemplos = Prueba.query.filter(Prueba.precio > 0).limit(8).all()
            for p in ejemplos:
                print(f"   • {p.nombre}: ${p.precio}")

            if con_precio > 8:
                print(f"   ... y {con_precio - 8} más")

            # Confirmación
            print(f"\n⚠️  Se actualizarán {con_precio} pruebas a precio 0.00")
            confirmacion = input("¿Continuar? (SI/NO): ")

            if confirmacion.upper() != "SI":
                print("❌ Operación cancelada")
                return

            # Actualizar
            print("\n⚡ Actualizando precios...")

            actualizadas = 0
            for prueba in Prueba.query.filter(Prueba.precio > 0).all():
                prueba.precio = 0.0
                actualizadas += 1

            db.session.commit()

            # Verificar
            restantes = Prueba.query.filter(Prueba.precio > 0).count()

            print(f"✅ Actualización completada!")
            print(f"📊 Pruebas actualizadas: {actualizadas}")
            print(f"📊 Pruebas con precio > 0 ahora: {restantes}")

            if restantes == 0:
                print(f"\n🎉 ¡TODOS LOS PRECIOS ELIMINADOS EXITOSAMENTE!")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("=" * 70)

if __name__ == "__main__":
    main()
