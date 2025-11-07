#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para inspeccionar completamente la base de datos
"""

import sqlite3
import os

db_path = "laboratorio.db"

if not os.path.exists(db_path):
    print(f"❌ No existe el archivo: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 70)
print("🔍 INSPECCIÓN COMPLETA DE LA BASE DE DATOS")
print("=" * 70)

# 1. Ver todas las tablas
print("\n📋 TABLAS EN LA BASE DE DATOS:")
print("-" * 70)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tablas = cursor.fetchall()

if not tablas:
    print("   ⚠️  No hay tablas en la base de datos")
else:
    for tabla in tablas:
        print(f"   ✅ {tabla[0]}")

# 2. Ver estructura de cada tabla
for tabla in tablas:
    nombre_tabla = tabla[0]
    print(f"\n📊 ESTRUCTURA DE '{nombre_tabla}':")
    print("-" * 70)

    cursor.execute(f"PRAGMA table_info({nombre_tabla})")
    columnas = cursor.fetchall()

    if not columnas:
        print("   ⚠️  Sin columnas")
    else:
        print(f"   {'Columna':<20} {'Tipo':<15} {'Null':<8} {'Default':<15}")
        print("   " + "-" * 60)
        for col in columnas:
            nombre_col = col[1]
            tipo = col[2]
            not_null = "NO" if col[3] else "SI"
            default = str(col[4]) if col[4] else ""
            print(f"   {nombre_col:<20} {tipo:<15} {not_null:<8} {default:<15}")

    # Contar registros
    cursor.execute(f"SELECT COUNT(*) FROM {nombre_tabla}")
    count = cursor.fetchone()[0]
    print(f"\n   📊 Total de registros: {count}")

    # Si es la tabla pruebas, mostrar algunos ejemplos
    if nombre_tabla == "pruebas" and count > 0:
        print(f"\n   📝 Primeros 3 registros:")
        cursor.execute(f"SELECT * FROM {nombre_tabla} LIMIT 3")
        registros = cursor.fetchall()
        for i, reg in enumerate(registros, 1):
            print(f"      {i}. {reg}")

conn.close()

print("\n" + "=" * 70)
print("✅ INSPECCIÓN COMPLETADA")
print("=" * 70)
