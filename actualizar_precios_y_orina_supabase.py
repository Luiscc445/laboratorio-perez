#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para:
1. Eliminar todos los precios (ponerlos en 0.00)
2. Cambiar la imagen del examen de ORINA en Supabase
"""

import sys
import os
import time
import requests
import hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Prueba

# API Key de Pexels
PEXELS_API_KEY = "pc4Lf88y25rYxtlfQmAcY1CZ4XOMq5b4tqWrfEk6cxWW5TyzKuWVPFp9"

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
    print("🔧 ACTUALIZACIÓN DE PRECIOS E IMAGEN DE ORINA - SUPABASE")
    print("=" * 70)

    app = create_app()

    with app.app_context():
        # PASO 1: ELIMINAR TODOS LOS PRECIOS
        print("\n📋 Paso 1: Eliminar todos los precios")
        print("-" * 70)

        try:
            total = Prueba.query.count()
            print(f"   📊 Total de pruebas: {total}")

            con_precio = Prueba.query.filter(Prueba.precio > 0).count()
            print(f"   💵 Pruebas con precio > 0: {con_precio}")

            if con_precio == 0:
                print("   ✅ Todos los precios ya están en 0.00")
            else:
                # Mostrar ejemplos
                ejemplos = Prueba.query.filter(Prueba.precio > 0).limit(5).all()
                print(f"\n   📝 Ejemplos de pruebas con precio:")
                for p in ejemplos:
                    print(f"      • {p.nombre} ({p.categoria}): ${p.precio}")

                # Confirmación
                print(f"\n   ⚠️  Se actualizarán {con_precio} pruebas a precio 0.00")
                confirmacion = input("   ¿Continuar? (SI/NO): ")

                if confirmacion.upper() != "SI":
                    print("   ❌ Operación cancelada")
                    return

                # Actualizar precios
                print("\n   ⚡ Actualizando precios...")

                # Actualizar usando ORM (más compatible)
                for prueba in Prueba.query.filter(Prueba.precio > 0).all():
                    prueba.precio = 0.0

                db.session.commit()

                # Verificar
                restantes = Prueba.query.filter(Prueba.precio > 0).count()
                print(f"   ✅ Precios actualizados!")
                print(f"   📊 Pruebas con precio > 0 ahora: {restantes}")

        except Exception as e:
            db.session.rollback()
            print(f"   ❌ Error: {str(e)}")
            return

        # PASO 2: CAMBIAR IMAGEN DE ORINA
        print("\n🖼️  Paso 2: Cambiar imagen del examen de ORINA")
        print("-" * 70)

        try:
            # Buscar prueba de ORINA
            orina = Prueba.query.filter(
                Prueba.nombre.ilike('%EXAMEN GENERAL DE ORINA%')
            ).first()

            if not orina:
                print("   ❌ No se encontró el examen de ORINA")
                return

            print(f"   📌 Encontrada: {orina.nombre}")
            print(f"   🆔 ID: {orina.id}")
            print(f"   📂 Categoría: {orina.categoria}")
            print(f"   🖼️  Imagen actual: {orina.imagen}")

            # Buscar nueva imagen en Pexels
            print(f"\n   🔍 Buscando nueva imagen en Pexels...")

            keywords_opciones = [
                "urine sample laboratory test tube container medical",
                "urinalysis laboratory testing equipment clinical",
                "urine test medical lab specimen collection",
                "laboratory urine analysis dipstick test",
                "clinical laboratory urine sample tube"
            ]

            imagen_url = None
            photo_id = None

            for idx, keywords in enumerate(keywords_opciones, 1):
                print(f"      Intento {idx}: '{keywords}'")
                imagen_url, photo_id = buscar_imagen_pexels(keywords, PEXELS_API_KEY)
                if imagen_url:
                    print(f"      ✅ Imagen encontrada! (ID: {photo_id})")
                    break
                time.sleep(1)

            if not imagen_url:
                print("   ❌ No se pudo encontrar una nueva imagen en Pexels")
                return

            # Descargar imagen
            hash_base = hashlib.md5(f"orina_{photo_id}".encode()).hexdigest()[:12]
            nombre_archivo = f"orina_{hash_base}.jpg"

            print(f"\n   ⬇️  Descargando nueva imagen...")
            print(f"      Archivo: {nombre_archivo}")

            if descargar_imagen(imagen_url, nombre_archivo):
                # Actualizar en la base de datos
                imagen_anterior = orina.imagen
                orina.imagen = nombre_archivo
                db.session.commit()

                print(f"   ✅ Imagen actualizada exitosamente!")
                print(f"      Anterior: {imagen_anterior}")
                print(f"      Nueva: {orina.imagen}")
            else:
                print("   ❌ Error al descargar la imagen")

        except Exception as e:
            db.session.rollback()
            print(f"   ❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("=" * 70)

if __name__ == "__main__":
    main()
