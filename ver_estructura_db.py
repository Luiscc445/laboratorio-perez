#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ver la estructura de la tabla pruebas
"""

import sqlite3

db_path = "laboratorio.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Ver estructura de la tabla
cursor.execute("PRAGMA table_info(pruebas)")
columnas = cursor.fetchall()

print("=" * 70)
print("📋 ESTRUCTURA DE LA TABLA 'pruebas'")
print("=" * 70)

for col in columnas:
    print(f"  {col[1]:20} | {col[2]:15} | Null: {not col[3]} | Default: {col[4]}")

conn.close()
