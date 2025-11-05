#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SCRIPT SEGURO - SIGUIENTES 60 PRUEBAS
NO ELIMINA NADA - Solo AGREGA pruebas nuevas
Las 55 primeras se mantienen intactas
"""

import os
import requests
import time
import hashlib
from app import create_app, db
from app.models import Prueba

PEXELS_API_KEY = "pc4Lf88y25rYxtlfQmAcY1CZ4XOMq5b4tqWrfEk6cxWW5TyzKuWVPFp9"

print("\n" + "="*80)
print("   🔬 SCRIPT SEGURO - SIGUIENTES 60 PRUEBAS")
print("="*80)
print("\n⚠️  IMPORTANTE:")
print("  ✅ NO elimina pruebas existentes")
print("  ✅ Solo AGREGA pruebas nuevas")
print("  ✅ Tus 55 pruebas actuales están SEGURAS")
print("  ✅ Verifica que no existan antes de crear")
print("\n⏱️  Tiempo: ~5-7 minutos (60 imágenes)")
print("="*80 + "\n")

confirmacion = input("¿Continuar? (escribe 'SI'): ")
if confirmacion.upper() != "SI":
    print("❌ Cancelado.")
    exit()

# SIGUIENTES 60 PRUEBAS (después de las primeras 55)
PRUEBAS_DATA = {
    "ALERGIAS": [
        "PANEL DE ALÉRGENOS AMBIENTALES",
        "PANEL DE ALÉRGENOS ALIMENTICIOS"
    ],
    "MARCADORES ONCOLÓGICOS": [
        "ALFA FETO PROTEÍNA (AFP)",
        "ANTÍGENO CARCINOEMBRIONARIO (CEA)",
        "CA 125",
        "CA 19-9",
        "CA 15-3",
        "PSA TOTAL",
        "PSA LIBRE",
        "HCG TUMORAL"
    ],
    "BACTERIOLOGÍA": [
        "CULTIVO Y ANTIBIOGRAMA",
        "CULTIVO Y ANTIBIOGRAMA PARA MYCOPLASMA Y UREAPLASMA",
        "EXAMEN EN FRESCO",
        "TINCIÓN DE GRAM",
        "MICOLÓGICO DIRECTO",
        "MICOLÓGICO CULTIVO",
        "BACILOSCOPIA SERIADO X 3"
    ],
    "ORINA": [
        "EXAMEN GENERAL DE ORINA (EGO)",
        "MORFOLOGÍA ERITROCITARIA",
        "CÁLCULO RENAL",
        "DEPURACIÓN DE CREATININA",
        "COCAÍNA",
        "MARIHUANA"
    ],
    "VITAMINAS": [
        "VITAMINA B12",
        "VITAMINA D (25 HIDROXIVITAMINA D)"
    ],
    "MATERIA FECAL": [
        "PARASITOLÓGICO SIMPLE",
        "PARASITOLÓGICO SERIADO X 3",
        "MOCO FECAL",
        "SANGRE OCULTA",
        "SANGRE OCULTA SERIADO X3",
        "TEST DE GRAHAM SERIADO X3",
        "AZÚCARES REDUCTORES",
        "ANTÍGENO GIARDIA (ELISA)",
        "AMEBA HISTOLYTICA (ELISA)",
        "H. PYLORI HECES",
        "ROTAVIRUS",
        "ADENOVIRUS"
    ],
    "PERFIL PRE-OPERATORIO": [
        "HEMOGRAMA, GRUPO SANGUÍNEO Y RH",
        "TIEMPO DE SANGRE Y COAGULACIÓN",
        "TIEMPO DE PROTROMBINA INR",
        "GLUCOSA, CREATININA, NUS, EXAMEN GENERAL DE ORINA"
    ],
    "PERFIL REUMATOIDEO": [
        "HEMOGRAMA, FACTOR REUMATOIDE (FR)",
        "PROTEÍNA C REACTIVA (PCR)",
        "ANTI-ESTREPTOLISINA O (ASTO)",
        "ÁCIDO ÚRICO",
        "ANTIPÉPTIDO CITRULINADO (CCP)"
    ],
    "PERFIL HEPÁTICO": [
        "HEMOGRAMA, TIEMPO DE PROTROMBINA",
        "PROTEÍNAS TOTALES Y FRACCIONES",
        "TRANSAMINASAS",
        "BILIRRUBINAS",
        "FOSFATASA ALCALINA",
        "GAMMA GLUTAMIL TRANSPEPTIDASA",
        "LACTATO DESHIDROGENASA"
    ]
}

PRECIOS_POR_CATEGORIA = {
    "ALERGIAS": 350.0,
    "MARCADORES ONCOLÓGICOS": 180.0,
    "BACTERIOLOGÍA": 150.0,
    "ORINA": 50.0,
    "VITAMINAS": 110.0,
    "MATERIA FECAL": 60.0,
    "PERFIL PRE-OPERATORIO": 200.0,
    "PERFIL REUMATOIDEO": 250.0,
    "PERFIL HEPÁTICO": 280.0
}

imagenes_usadas = set()


def analizar_prueba_inteligente(nombre_prueba, categoria):
    """Análisis inteligente de keywords"""
    nombre_upper = nombre_prueba.upper()

    mapeo_especifico = {
        "ALÉRGENOS AMBIENTALES": "allergy test laboratory skin prick environmental pollen",
        "ALÉRGENOS ALIMENTICIOS": "food allergy test laboratory panel skin",

        "ALFA FETO PROTEÍNA": "AFP tumor marker test laboratory vial cancer",
        "CARCINOEMBRIONARIO": "CEA tumor marker laboratory test cancer tubes",
        "CA 125": "ovarian cancer tumor marker test laboratory CA125",
        "CA 19-9": "pancreatic tumor marker laboratory test CA19",
        "CA 15-3": "breast tumor marker laboratory test CA15",
        "PSA TOTAL": "prostate test laboratory PSA marker blood",
        "PSA LIBRE": "prostate PSA test laboratory free tubes",
        "HCG TUMORAL": "tumor marker test laboratory HCG vial",

        "CULTIVO Y ANTIBIOGRAMA": "bacterial culture petri dish laboratory antibiotic",
        "MYCOPLASMA": "bacterial culture laboratory microscope mycoplasma",
        "EXAMEN FRESCO": "microscope slide laboratory fresh sample wet",
        "TINCIÓN GRAM": "gram stain microscope bacteria slide purple",
        "MICOLÓGICO DIRECTO": "fungal microscope laboratory slide direct",
        "MICOLÓGICO CULTIVO": "fungal culture laboratory petri dish mold",
        "BACILOSCOPIA": "tuberculosis microscope slide stain red TB",

        "ORINA": "urine test laboratory sample container yellow",
        "MORFOLOGÍA ERITROCITARIA": "urine microscope red cells sediment",
        "CÁLCULO RENAL": "kidney stone laboratory crystals urine",
        "DEPURACIÓN CREATININA": "kidney function test laboratory creatinine",
        "COCAÍNA": "drug test laboratory urine screening cocaine",
        "MARIHUANA": "drug screening test laboratory urine cannabis",

        "VITAMINA B12": "vitamin B12 supplement laboratory test red",
        "VITAMINA D": "vitamin D test laboratory analysis sunshine",

        "PARASITOLÓGICO": "parasite microscope laboratory stool ova",
        "MOCO FECAL": "stool sample laboratory test container fecal",
        "SANGRE OCULTA": "occult blood test laboratory stool hidden",
        "GRAHAM": "pinworm test laboratory tape slide cellulose",
        "AZÚCARES REDUCTORES": "sugar test laboratory chemistry reducing",
        "GIARDIA": "giardia parasite microscope laboratory protozoa",
        "AMEBA": "amoeba parasite microscope laboratory entamoeba",
        "PYLORI HECES": "H pylori test laboratory stool antigen",
        "ROTAVIRUS": "rotavirus test laboratory sample kit",
        "ADENOVIRUS": "adenovirus laboratory test sample rapid",

        "PRE-OPERATORIO": "preoperative laboratory blood test tubes surgery",
        "REUMATOIDE": "rheumatoid factor test laboratory arthritis tubes",
        "PROTEÍNA C REACTIVA": "CRP test laboratory inflammation marker tubes",
        "ESTREPTOLISINA": "ASTO test laboratory strep antibody tubes",
        "CITRULINADO": "rheumatoid arthritis test laboratory CCP antibody",

        "HEPÁTICO": "liver function laboratory test tubes hepatic",
        "TRANSAMINASAS": "liver enzyme test laboratory tubes ALT AST",
        "BILIRRUBINAS": "bilirubin test laboratory yellow sample jaundice",
        "FOSFATASA ALCALINA": "alkaline phosphatase test laboratory chemistry",
        "GAMMA GLUTAMIL": "GGT liver enzyme test laboratory tubes"
    }

    for termino, keywords in mapeo_especifico.items():
        if termino in nombre_upper:
            return keywords

    categoria_keywords = {
        "ALERGIAS": "allergy laboratory test panel skin prick",
        "MARCADORES ONCOLÓGICOS": "tumor marker laboratory test cancer vial",
        "BACTERIOLOGÍA": "bacteria culture petri dish laboratory microscope",
        "ORINA": "urine laboratory test sample container",
        "VITAMINAS": "vitamin laboratory test supplement bottle",
        "MATERIA FECAL": "laboratory stool sample test container",
        "PERFIL PRE-OPERATORIO": "preoperative laboratory blood test tubes",
        "PERFIL REUMATOIDEO": "laboratory test tubes rheumatoid arthritis",
        "PERFIL HEPÁTICO": "liver function laboratory test tubes hepatic"
    }

    return categoria_keywords.get(categoria, "medical laboratory test equipment")


def buscar_imagen_unica_pexels(keywords, api_key, intentos=3):
    """Busca imagen única en Pexels"""
    for pagina in range(1, intentos + 1):
        try:
            url = "https://api.pexels.com/v1/search"
            headers = {"Authorization": api_key}
            params = {
                "query": keywords,
                "per_page": 5,
                "page": pagina,
                "orientation": "landscape"
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data.get("photos") and len(data["photos"]) > 0:
                for photo in data["photos"]:
                    photo_id = photo["id"]
                    if photo_id not in imagenes_usadas:
                        imagenes_usadas.add(photo_id)
                        return photo["src"]["medium"], photo_id
                continue
            else:
                return None, None

        except Exception as e:
            print(f" ❌ Error: {str(e)}")
            return None, None

    return None, None


def descargar_imagen(url, nombre_archivo, directorio):
    """Descarga imagen"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        ruta_completa = os.path.join(directorio, nombre_archivo)
        with open(ruta_completa, 'wb') as f:
            f.write(response.content)

        return nombre_archivo
    except Exception as e:
        print(f" ❌ Error: {str(e)}")
        return None


def generar_nombre_unico(nombre_prueba, photo_id):
    """Genera nombre único"""
    hash_obj = hashlib.md5(nombre_prueba.encode())
    return f"prueba_{hash_obj.hexdigest()[:8]}_{photo_id}.jpg"


def main():
    app = create_app()

    with app.app_context():
        # IMPORTANTE: Contar pruebas existentes
        pruebas_existentes = Prueba.query.count()
        print(f"\n📊 Pruebas existentes en DB: {pruebas_existentes}")
        print("✅ Estas pruebas NO serán eliminadas\n")

        print("📁 PASO 1/2: Verificando directorio...")
        dir_imagenes = os.path.join('app', 'static', 'uploads', 'pruebas')
        os.makedirs(dir_imagenes, exist_ok=True)
        print(f"✅ {dir_imagenes}\n")

        total_pruebas = sum(len(p) for p in PRUEBAS_DATA.values())
        print(f"🔬 PASO 2/2: Agregando {total_pruebas} pruebas nuevas...")
        print("(Tiempo estimado: ~5-7 minutos)\n")

        contador = 0
        agregadas = 0
        existian = 0
        imagenes_ok = 0

        for categoria, pruebas in PRUEBAS_DATA.items():
            print(f"📂 {categoria} ({len(pruebas)} pruebas)")
            precio = PRECIOS_POR_CATEGORIA.get(categoria, 100.0)

            for nombre_prueba in pruebas:
                contador += 1
                print(f"  [{contador}/{total_pruebas}] {nombre_prueba[:40]}...")

                # VERIFICAR SI YA EXISTE (SEGURIDAD)
                existe = Prueba.query.filter_by(
                    nombre=nombre_prueba,
                    categoria=categoria
                ).first()

                if existe:
                    print(f"      ⚠️  Ya existe (se mantiene)")
                    existian += 1
                    continue

                # Buscar imagen
                keywords = analizar_prueba_inteligente(nombre_prueba, categoria)
                print(f"      🔍 {keywords[:60]}...")

                url_imagen, photo_id = buscar_imagen_unica_pexels(keywords, PEXELS_API_KEY)

                nombre_imagen = None
                if url_imagen and photo_id:
                    nombre_imagen = generar_nombre_unico(nombre_prueba, photo_id)
                    resultado = descargar_imagen(url_imagen, nombre_imagen, dir_imagenes)
                    if resultado:
                        print(f"      ✅ ID: {photo_id}")
                        imagenes_ok += 1
                    else:
                        print(f"      ⚠️ Error descarga")
                        nombre_imagen = None
                else:
                    print(f"      ⚠️ No encontrada")

                # Crear NUEVA prueba
                nueva_prueba = Prueba(
                    nombre=nombre_prueba,
                    categoria=categoria,
                    precio=precio,
                    descripcion=f"Prueba de {categoria.lower()}: {nombre_prueba}",
                    imagen=nombre_imagen
                )
                db.session.add(nueva_prueba)
                agregadas += 1

                time.sleep(1)

            print()

        print("\n💾 Guardando nuevas pruebas...")
        db.session.commit()

        total_final = Prueba.query.count()

        print("\n" + "="*80)
        print("✨ ¡COMPLETADO SEGURO!")
        print("="*80)
        print(f"📊 Pruebas que ya existían: {pruebas_existentes}")
        print(f"✅ Pruebas nuevas agregadas: {agregadas}")
        print(f"⚠️  Pruebas que ya existían (no duplicadas): {existian}")
        print(f"🖼️  Imágenes únicas descargadas: {imagenes_ok}")
        print(f"📊 TOTAL en DB ahora: {total_final}")
        print("="*80)
        print("\n🎉 ¡Nuevas pruebas agregadas sin perder las anteriores!")
        print("💡 Ejecuta: python run.py\n")


if __name__ == "__main__":
    main()
