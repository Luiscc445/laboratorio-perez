#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 TRUCO RÁPIDO: Eliminar TODOS los precios usando SQL directo
"""

import sqlite3
import os

def main():
    print("=" * 70)
    print("⚡ ELIMINACIÓN RÁPIDA DE PRECIOS (SQL DIRECTO)")
    print("=" * 70)

    db_path = "laboratorio.db"

    if not os.path.exists(db_path):
        print(f"❌ No se encontró la base de datos: {db_path}")
        return

    print(f"\n📂 Base de datos encontrada: {db_path}")

    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Contar pruebas antes
    cursor.execute("SELECT COUNT(*) FROM pruebas")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pruebas WHERE precio > 0")
    con_precio = cursor.fetchone()[0]

    print(f"📊 Total de pruebas: {total}")
    print(f"💰 Pruebas con precio > 0: {con_precio}")

    if con_precio == 0:
        print("\n✅ Todos los precios ya están en 0.00")
        conn.close()
        return

    # Confirmación
    print(f"\n⚠️  Se actualizarán {con_precio} pruebas a precio 0.00")
    confirmacion = input("¿Continuar? (SI/NO): ")

    if confirmacion.upper() != "SI":
        print("❌ Operación cancelada")
        conn.close()
        return

    # Ejecutar UPDATE masivo
    print("\n⚡ Ejecutando actualización masiva...")

    cursor.execute("UPDATE pruebas SET precio = 0.0")
    conn.commit()

    # Verificar
    cursor.execute("SELECT COUNT(*) FROM pruebas WHERE precio > 0")
    restantes = cursor.fetchone()[0]

    print(f"✅ Actualización completada!")
    print(f"📊 Pruebas con precio > 0 ahora: {restantes}")

    conn.close()

    print("\n" + "=" * 70)
    print("✅ PRECIOS ELIMINADOS EXITOSAMENTE")
    print("=" * 70)

if __name__ == "__main__":
    main()
