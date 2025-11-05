#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SCRIPT INTELIGENTE - SOLO 60 PRUEBAS
Para evitar cortes, procesamos solo las primeras 60 pruebas
"""

import os
import requests
import time
import hashlib
from app import create_app, db
from app.models import Prueba

PEXELS_API_KEY = "pc4Lf88y25rYxtlfQmAcY1CZ4XOMq5b4tqWrfEk6cxWW5TyzKuWVPFp9"

print("\n" + "="*80)
print("   🔬 SCRIPT INTELIGENTE - PRIMERAS 60 PRUEBAS")
print("="*80)
print("\nCaracterísticas:")
print("  ✅ Procesa solo 60 pruebas (evita cortes)")
print("  ✅ Análisis inteligente por prueba")
print("  ✅ Keywords específicos técnicos")
print("  ✅ NO repite imágenes (verifica IDs)")
print("  ✅ Solo imágenes técnicas de laboratorio")
print("\n⏱️  Tiempo: ~5-7 minutos (60 imágenes)")
print("="*80 + "\n")

confirmacion = input("¿Continuar? (escribe 'SI'): ")
if confirmacion.upper() != "SI":
    print("❌ Cancelado.")
    exit()

# SOLO LAS PRIMERAS 60 PRUEBAS
PRUEBAS_DATA = {
    "HEMATOLOGÍA": [
        "HEMOGRAMA",
        "VELOCIDAD DE SEDIMENTACIÓN (VES)",
        "HEMOGLOBINA-HEMATOCRITO",
        "RECUENTO PLAQUETAS",
        "RECUENTO RETICULOCITOS",
        "GRUPO SANGUÍNEO Y FACTOR RH",
        "COOMBS DIRECTO",
        "COOMBS INDIRECTO",
        "HIERRO SÉRICO",
        "FERRITINA",
        "TRANSFERRINA"
    ],
    "COAGULACIÓN": [
        "TIEMPO DE PROTROMBINA (INR)",
        "TIEMPO DE TROMBOPLASTINA",
        "TIEMPO DE TROMBINA",
        "TIEMPO DE SANGRE Y COAGULACIÓN",
        "DÍMERO D"
    ],
    "BIOQUÍMICA CLÍNICA": [
        "GLUCOSA BASAL O POST-PRAND.",
        "TOLERANCIA A LA GLUCOSA",
        "HEMOGLOBINA GLICOSILADA (HbA1c)",
        "NUS (BUN)",
        "UREA",
        "CREATININA",
        "ÁCIDO ÚRICO",
        "COLESTEROL TOTAL",
        "COLESTEROL HDL, LDL, VLDL",
        "TRIGLICÉRIDOS",
        "AMILASA",
        "LIPASA",
        "TRANSAMINASAS (GOT-GPT)",
        "BILIRRUBINAS (T,D,I)",
        "FOSFATASA ALCALINA",
        "GAMMA GLUTAMIL TRANSPEPTIDASA (GGT)",
        "LACTATO DESHIDROGENASA (LDH)",
        "FOSFATASA ÁCIDA TOTAL",
        "CPK TOTAL",
        "CPK-MB",
        "TROPONINA C",
        "PROTEÍNAS TOTALES Y FRACCIONES"
    ],
    "ELECTROLITOS": [
        "CALCIO SÉRICO",
        "CALCIO IÓNICO",
        "MAGNESIO",
        "FÓSFORO",
        "ELECTROLITOS (Na, K, Cl)"
    ],
    "ENDOCRINOLOGÍA": [
        "TSH",
        "T3",
        "T4",
        "T3 LIBRE",
        "T4 LIBRE",
        "ANTI-TIROPEROXIDASA (ANTI-TPO)",
        "HORMONA LUTEINIZANTE (LH)",
        "HORMONA FOLÍCULO ESTIMULANTE (FSH)",
        "ESTRADIOL (E2)",
        "PROGESTERONA",
        "TESTOSTERONA TOTAL O LIBRE",
        "PROLACTINA (PRL)"
    ]
}

PRECIOS_POR_CATEGORIA = {
    "HEMATOLOGÍA": 80.0,
    "COAGULACIÓN": 100.0,
    "BIOQUÍMICA CLÍNICA": 90.0,
    "ELECTROLITOS": 85.0,
    "ENDOCRINOLOGÍA": 120.0
}

imagenes_usadas = set()


def analizar_prueba_inteligente(nombre_prueba, categoria):
    """Análisis inteligente de keywords"""
    nombre_upper = nombre_prueba.upper()

    mapeo_especifico = {
        "HEMOGRAMA": "blood cells microscope laboratory slide red",
        "VELOCIDAD DE SEDIMENTACIÓN": "laboratory test tube blood sedimentation equipment",
        "HEMOGLOBINA": "red blood cells microscope hemoglobin laboratory",
        "HEMATOCRITO": "blood sample centrifuge hematocrit tube laboratory",
        "PLAQUETAS": "platelets microscope blood cells laboratory",
        "RETICULOCITOS": "reticulocytes blood cells stain microscope",
        "GRUPO SANGUÍNEO": "blood type test laboratory tubes typing",
        "COOMBS": "laboratory blood test tubes reagent coombs",
        "HIERRO": "iron supplement laboratory test serum",
        "FERRITINA": "laboratory test tube chemistry ferritin analysis",
        "TRANSFERRINA": "laboratory test sample analysis transferrin",

        "PROTROMBINA": "blood clotting test laboratory equipment prothrombin",
        "TROMBOPLASTINA": "coagulation test laboratory tubes thromboplastin",
        "TROMBINA": "laboratory test coagulation thrombin analysis",
        "COAGULACIÓN": "blood clotting laboratory process coagulation",
        "DÍMERO": "laboratory test equipment d-dimer analysis",

        "GLUCOSA": "glucose meter test laboratory blood sugar diabetes",
        "TOLERANCIA GLUCOSA": "glucose test laboratory equipment meter tolerance",
        "HEMOGLOBINA GLICOSILADA": "diabetes test laboratory analysis HbA1c glycated",
        "UREA": "laboratory chemistry test tubes urea analysis",
        "CREATININA": "kidney function test laboratory chemistry creatinine",
        "ÁCIDO ÚRICO": "uric acid crystals microscope laboratory gout",
        "COLESTEROL": "cholesterol test laboratory tubes lipids hdl",
        "TRIGLICÉRIDOS": "lipid test laboratory chemistry triglycerides analysis",
        "AMILASA": "enzyme test laboratory pancreas amylase analysis",
        "LIPASA": "lipase test laboratory tubes chemistry pancreas",
        "TRANSAMINASAS": "liver function test laboratory tubes transaminase",
        "BILIRRUBINAS": "bilirubin test laboratory yellow sample liver",
        "FOSFATASA": "alkaline phosphatase test laboratory chemistry bone",
        "GGT": "liver enzyme test laboratory tubes gamma",
        "LDH": "lactate dehydrogenase laboratory test enzyme",
        "CPK": "creatine kinase test laboratory muscle enzyme heart",
        "TROPONINA": "troponin test laboratory cardiac marker heart",
        "PROTEÍNAS": "protein test laboratory chemistry analysis serum",

        "CALCIO": "calcium test laboratory chemistry minerals bones",
        "MAGNESIO": "magnesium test laboratory analysis minerals",
        "FÓSFORO": "phosphorus test laboratory chemistry phosphate",
        "ELECTROLITOS": "electrolytes test laboratory chemistry ions sodium",

        "TSH": "thyroid test laboratory hormone TSH analysis",
        "T3": "thyroid hormone test laboratory tubes T3",
        "T4": "thyroid test laboratory hormone T4 chemistry",
        "TIROPEROXIDASA": "thyroid antibody test laboratory TPO",
        "LUTEINIZANTE": "hormone test laboratory reproductive LH",
        "FOLÍCULO ESTIMULANTE": "FSH hormone test laboratory tubes follicle",
        "ESTRADIOL": "estrogen hormone test laboratory analysis estradiol",
        "PROGESTERONA": "progesterone hormone test laboratory reproductive",
        "TESTOSTERONA": "testosterone hormone test laboratory vial male",
        "PROLACTINA": "prolactin hormone test laboratory analysis pituitary"
    }

    for termino, keywords in mapeo_especifico.items():
        if termino in nombre_upper:
            return keywords

    categoria_keywords = {
        "HEMATOLOGÍA": "blood test laboratory microscope cells hematology",
        "COAGULACIÓN": "blood clotting laboratory test tubes coagulation",
        "BIOQUÍMICA CLÍNICA": "laboratory chemistry test tubes analysis biochemistry",
        "ELECTROLITOS": "laboratory chemistry minerals test electrolytes",
        "ENDOCRINOLOGÍA": "hormone laboratory test tubes endocrine"
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
        print("\n🗑️  PASO 1/3: Eliminando TODAS las pruebas existentes...")
        eliminadas = Prueba.query.delete()
        db.session.commit()
        print(f"✅ {eliminadas} pruebas eliminadas\n")

        print("📁 PASO 2/3: Creando directorio...")
        dir_imagenes = os.path.join('app', 'static', 'uploads', 'pruebas')
        os.makedirs(dir_imagenes, exist_ok=True)
        print(f"✅ {dir_imagenes}\n")

        total_pruebas = sum(len(p) for p in PRUEBAS_DATA.values())
        print(f"🔬 PASO 3/3: Creando {total_pruebas} pruebas con imágenes ÚNICAS...")
        print("(Tiempo estimado: ~5-7 minutos)\n")

        contador = 0
        imagenes_ok = 0

        for categoria, pruebas in PRUEBAS_DATA.items():
            print(f"📂 {categoria} ({len(pruebas)} pruebas)")
            precio = PRECIOS_POR_CATEGORIA.get(categoria, 100.0)

            for nombre_prueba in pruebas:
                contador += 1
                print(f"  [{contador}/{total_pruebas}] {nombre_prueba[:40]}...")

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

                nueva_prueba = Prueba(
                    nombre=nombre_prueba,
                    categoria=categoria,
                    precio=precio,
                    descripcion=f"Prueba de {categoria.lower()}: {nombre_prueba}",
                    imagen=nombre_imagen
                )
                db.session.add(nueva_prueba)

                time.sleep(1)

            print()

        print("\n💾 Guardando...")
        db.session.commit()

        print("\n" + "="*80)
        print("✨ ¡COMPLETADO!")
        print("="*80)
        print(f"✅ Pruebas creadas: {contador}")
        print(f"🖼️  Imágenes únicas: {imagenes_ok}")
        print(f"📊 Total en DB: {Prueba.query.count()}")
        print("="*80)
        print("\n🎉 ¡60 pruebas con imágenes profesionales únicas!")
        print("💡 Ejecuta: python run.py\n")


if __name__ == "__main__":
    main()
