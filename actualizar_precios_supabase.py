#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar precios en Supabase PostgreSQL
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Prueba

def main():
    print("=" * 70)
    print("💰 ELIMINAR TODOS LOS PRECIOS - SUPABASE")
    print("=" * 70)

    # Crear app con configuración de Supabase
    app = create_app()

    with app.app_context():
        # Verificar conexión
        try:
            total = Prueba.query.count()
            print(f"\n✅ Conectado a Supabase")
            print(f"📊 Total de pruebas: {total}")
        except Exception as e:
            print(f"❌ Error conectando a Supabase: {str(e)}")
            print("\n💡 Verifica que tu archivo .env tenga la DATABASE_URL correcta")
            return

        if total == 0:
            print("\n⚠️  No hay pruebas en la base de datos")
            return

        # Contar pruebas con precio
        con_precio = Prueba.query.filter(Prueba.precio > 0).count()
        print(f"💵 Pruebas con precio > 0: {con_precio}")

        if con_precio == 0:
            print("\n✅ Todos los precios ya están en 0.00")
            return

        # Mostrar algunos ejemplos
        ejemplos = Prueba.query.filter(Prueba.precio > 0).limit(5).all()
        if ejemplos:
            print(f"\n📋 Ejemplos de pruebas con precio:")
            for p in ejemplos:
                print(f"   • {p.nombre} ({p.categoria}): ${p.precio}")

        # Confirmación
        print(f"\n⚠️  Se actualizarán {con_precio} pruebas a precio 0.00")
        confirmacion = input("¿Continuar? (SI/NO): ")

        if confirmacion.upper() != "SI":
            print("❌ Operación cancelada")
            return

        # Actualizar usando SQL directo (más rápido)
        print("\n⚡ Actualizando precios...")

        try:
            # Ejecutar UPDATE directo
            db.session.execute(db.text("UPDATE pruebas SET precio = 0.0 WHERE precio > 0"))
            db.session.commit()

            # Verificar
            restantes = Prueba.query.filter(Prueba.precio > 0).count()

            print(f"✅ Actualización completada!")
            print(f"📊 Pruebas con precio > 0 ahora: {restantes}")

            if restantes == 0:
                print(f"🎉 ¡Todos los precios eliminados exitosamente!")
            else:
                print(f"⚠️  Aún quedan {restantes} pruebas con precio")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Error actualizando: {str(e)}")
            return

    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("=" * 70)

if __name__ == "__main__":
    main()
