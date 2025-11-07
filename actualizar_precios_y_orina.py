#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para:
1. Eliminar todos los precios (ponerlos en 0.00)
2. Cambiar la imagen del examen de ORINA
"""

import os
import sys
import time
import requests
import hashlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuración
PEXELS_API_KEY = "pc4Lf88y25rYxtlfQmAcY1CZ4XOMq5b4tqWrfEk6cxWW5TyzKuWVPFp9"

# Crear app Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laboratorio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo - Solo columnas que existen en la DB
class Prueba(db.Model):
    __tablename__ = 'pruebas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100))
    precio = db.Column(db.Float, default=0.0)
    imagen = db.Column(db.String(200))
    fecha_creacion = db.Column(db.DateTime)

def buscar_imagen_pexels(keywords, api_key):
    """Busca una imagen en Pexels"""
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": api_key}
    params = {
        "query": keywords,
        "per_page": 5,
        "page": 1
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("photos"):
                return data["photos"][0]["src"]["medium"], data["photos"][0]["id"]
        return None, None
    except Exception as e:
        print(f"    ❌ Error buscando imagen: {str(e)}")
        return None, None

def descargar_imagen(url, nombre_archivo):
    """Descarga una imagen desde URL"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            ruta = os.path.join("app", "static", "img", "pruebas", nombre_archivo)
            os.makedirs(os.path.dirname(ruta), exist_ok=True)

            with open(ruta, 'wb') as f:
                f.write(response.content)
            return True
        return False
    except Exception as e:
        print(f"    ❌ Error descargando: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("🔧 ACTUALIZACIÓN DE PRECIOS E IMAGEN DE ORINA")
    print("=" * 70)

    with app.app_context():
        # 1. ELIMINAR TODOS LOS PRECIOS
        print("\n📋 Paso 1: Eliminar todos los precios")
        print("-" * 70)

        todas_pruebas = Prueba.query.all()
        total = len(todas_pruebas)

        print(f"   Encontradas {total} pruebas en la base de datos")

        confirmacion = input("\n⚠️  ¿Desea poner TODOS los precios en 0.00? (SI/NO): ")

        if confirmacion.upper() != "SI":
            print("❌ Operación cancelada")
            return

        actualizadas = 0
        for prueba in todas_pruebas:
            if prueba.precio != 0.0:
                prueba.precio = 0.0
                actualizadas += 1

        db.session.commit()
        print(f"   ✅ {actualizadas} precios actualizados a 0.00")
        print(f"   📊 {total - actualizadas} ya estaban en 0.00")

        # 2. CAMBIAR IMAGEN DE ORINA
        print("\n🖼️  Paso 2: Cambiar imagen del examen de ORINA")
        print("-" * 70)

        prueba_orina = Prueba.query.filter_by(
            nombre="EXAMEN GENERAL DE ORINA (EGO)",
            categoria="ORINA"
        ).first()

        if not prueba_orina:
            print("   ❌ No se encontró el examen de ORINA en la base de datos")
            return

        print(f"   📌 Encontrada: {prueba_orina.nombre}")
        print(f"   🖼️  Imagen actual: {prueba_orina.imagen}")

        # Nuevos keywords más específicos para ORINA
        keywords_opciones = [
            "urine sample laboratory test tube container",
            "urinalysis laboratory testing equipment",
            "urine test medical lab specimen",
            "laboratory urine analysis dipstick",
            "clinical urine sample collection"
        ]

        print(f"\n   🔍 Buscando nueva imagen en Pexels...")

        imagen_url = None
        photo_id = None

        for idx, keywords in enumerate(keywords_opciones, 1):
            print(f"      Intento {idx}: '{keywords}'")
            imagen_url, photo_id = buscar_imagen_pexels(keywords, PEXELS_API_KEY)
            if imagen_url:
                print(f"      ✅ Imagen encontrada!")
                break
            time.sleep(1)

        if not imagen_url:
            print("   ❌ No se pudo encontrar una nueva imagen")
            return

        # Descargar imagen
        hash_base = hashlib.md5(f"orina_{photo_id}".encode()).hexdigest()[:12]
        nombre_archivo = f"orina_{hash_base}.jpg"

        print(f"   ⬇️  Descargando nueva imagen: {nombre_archivo}")

        if descargar_imagen(imagen_url, nombre_archivo):
            # Actualizar en la base de datos
            prueba_orina.imagen = f"img/pruebas/{nombre_archivo}"
            db.session.commit()

            print(f"   ✅ Imagen actualizada exitosamente!")
            print(f"   📁 Nueva ruta: {prueba_orina.imagen}")
        else:
            print("   ❌ Error al descargar la imagen")

    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("=" * 70)

if __name__ == "__main__":
    main()
