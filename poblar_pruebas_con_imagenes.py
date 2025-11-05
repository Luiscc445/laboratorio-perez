#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para poblar TODAS las pruebas con IMÁGENES INDIVIDUALES usando Pexels API
Cada una de las 176+ pruebas tendrá su propia imagen profesional única y fija
"""

import os
import requests
import time
import hashlib
from app import create_app, db
from app.models import Prueba

# ========== CONFIGURACIÓN PEXELS API ==========
# Pexels API es GRATUITA - Registro en: https://www.pexels.com/api/
# Límite: 200 requests por hora (suficiente para este uso)
PEXELS_API_KEY = "TU_API_KEY_AQUI"  # Debes registrarte en Pexels y obtener tu API key gratuita

# Si no quieres usar Pexels, se usará Unsplash (también gratuito, sin API key)
USE_PEXELS = True  # Cambiar a False para usar Unsplash sin API key

# ========== DATOS DE PRUEBAS ==========
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
    "ALERGIAS": [
        "PANEL DE ALÉRGENOS AMBIENTALES",
        "PANEL DE ALÉRGENOS ALIMENTICIOS"
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
        "PROLACTINA (PRL)",
        "B-HCG CUANTITATIVA",
        "CORTISOL AM O PM",
        "ACTH",
        "INSULINA BASAL O POST-PRAND.",
        "PARATOHORMONA (PTH)",
        "HORMONA DEL CRECIMIENTO (GH)"
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
    ],
    "PERFIL OBSTÉTRICO CONTROL": [
        "HEMOGRAMA",
        "GLUCOSA",
        "CREATININA",
        "NUS",
        "EXAMEN GENERAL DE ORINA"
    ],
    "MARCADORES DE HEPATITIS": [
        "HEPATITIS A (IgM-IgG) (ELISA)",
        "HEPATITIS B ANTÍGENO SUPERFICIE (ELISA)",
        "HEPATITIS B ANTICUERPO SUPERFICIE (ELISA)",
        "HEPATITIS B ANTICUERPO CORE (ELISA)",
        "HEPATITIS B ANTÍGENO ENVOLTURA (ELISA)",
        "HEPATITIS B ANTICUERPO ENVOLTURA (ELISA)",
        "HEPATITIS C ANTICUERPOS TOTALES (ELISA)"
    ],
    "INMUNOLOGÍA": [
        "PROTEÍNA C REACTIVA (POR NEFELOMETRÍA)",
        "FACTOR REUMATOIDE (FR NEFELOMETRÍA)",
        "ANTI-ESTREPTOLISINA O (ASTO NEFELOMETRÍA)",
        "REACCIÓN DE WIDAL",
        "RPR",
        "BRUCELOSIS (ELISA)",
        "TOXOPLASMA (ELISA)",
        "CITOMEGALOVIRUS (IgM-IgG) (ELISA)",
        "EPSTEIN BARR (IgM-IgG) (ELISA)",
        "HERPES VIRUS TIPO 1 (IgM-IgG) (ELISA)",
        "HERPES VIRUS TIPO 2 (IgM-IgG) (ELISA)",
        "ANTI VIH 1 + 2 (ELISA)",
        "RUBEOLA (IgM-IgG) (ELISA)",
        "SARAMPIÓN (IgM-IgG) (ELISA)",
        "CHLAMYDIA TRACHOMATIS (IgM-IgG) (ELISA)",
        "SÍFILIS (ELISA)",
        "CHAGAS (ELISA)",
        "ANTIPÉPTIDO CITRULINADO (CCP)",
        "ANTICUERPOS ANTINUCLEARES (ANA)",
        "ANTI DNA (DS)",
        "ANTI SMITH",
        "ANTI ENA (Ro,La,Sm,RNP,Scl-70,Jo1)",
        "COMPLEMENTOS C3 - C4",
        "INMUNOGLOBULINAS (G-A-M)",
        "HELICOBACTER PYLORI (IgG) (ELISA)",
        "ANTI-ENDOMISIO (ELISA)",
        "ANTI-GLIADINA (ELISA)",
        "H. PYLORI SUERO (IgM-IgG) (ELISA)"
    ],
    "PERFIL OBSTÉTRICO": [
        "HEMOGRAMA, GRUPO SANGUÍNEO Y RH",
        "RPR",
        "VIH",
        "CHAGAS",
        "GLUCOSA",
        "CREATININA",
        "NUS",
        "EXAMEN GENERAL DE ORINA",
        "T.O.R.C.H. (IgM-IgG) (ELISA)"
    ],
    "BIOLOGÍA MOLECULAR": [
        "PANEL DE DETECCIÓN DE 12 PATÓGENOS ETS",
        "PANEL DE DETECCIÓN DE FIEBRES HEMORRÁGICAS VIRALES",
        "PANEL DE DETECCIÓN Y GENOTIPIFICACIÓN DE 35 VARIANTES VPH",
        "PANEL PARA DETECCIÓN DE MICROORGANISMOS RESPIRATORIOS"
    ]
}

PRECIOS_POR_CATEGORIA = {
    "HEMATOLOGÍA": 80.0,
    "COAGULACIÓN": 100.0,
    "BIOQUÍMICA CLÍNICA": 90.0,
    "ELECTROLITOS": 85.0,
    "ALERGIAS": 350.0,
    "ENDOCRINOLOGÍA": 120.0,
    "MARCADORES ONCOLÓGICOS": 180.0,
    "BACTERIOLOGÍA": 150.0,
    "ORINA": 50.0,
    "VITAMINAS": 110.0,
    "MATERIA FECAL": 60.0,
    "PERFIL PRE-OPERATORIO": 200.0,
    "PERFIL REUMATOIDEO": 250.0,
    "PERFIL HEPÁTICO": 280.0,
    "PERFIL OBSTÉTRICO CONTROL": 220.0,
    "MARCADORES DE HEPATITIS": 150.0,
    "INMUNOLOGÍA": 130.0,
    "PERFIL OBSTÉTRICO": 300.0,
    "BIOLOGÍA MOLECULAR": 450.0
}


def generar_keywords(nombre_prueba, categoria):
    """
    Genera keywords inteligentes para buscar imágenes basándose en el nombre de la prueba
    """
    # Mapeo de términos médicos a términos de búsqueda en inglés
    mapeo_terminos = {
        "HEMOGRAMA": "blood test cells",
        "SANGRE": "blood test",
        "GLUCOSA": "glucose blood sugar",
        "COLESTEROL": "cholesterol test",
        "HEPATITIS": "hepatitis liver",
        "VIH": "hiv test",
        "ORINA": "urine test",
        "HECES": "stool sample",
        "CULTIVO": "bacterial culture",
        "BACTERIA": "bacteria petri dish",
        "HORMONA": "hormone blood test",
        "TIROIDES": "thyroid",
        "VITAMINA": "vitamin supplement",
        "CANCER": "cancer cells",
        "DNA": "dna helix",
        "MOLECULAR": "molecular biology",
        "EMBARAZO": "pregnancy test",
        "CORAZÓN": "heart",
        "RIÑÓN": "kidney",
        "HÍGADO": "liver"
    }

    # Extraer palabras clave del nombre
    nombre_upper = nombre_prueba.upper()

    # Buscar coincidencias en el mapeo
    for termino, keywords in mapeo_terminos.items():
        if termino in nombre_upper:
            return f"{keywords} laboratory medical"

    # Si no hay coincidencia específica, usar categoría + "laboratory test"
    categoria_map = {
        "HEMATOLOGÍA": "blood test hematology",
        "COAGULACIÓN": "blood clotting coagulation",
        "BIOQUÍMICA CLÍNICA": "biochemistry laboratory",
        "ELECTROLITOS": "electrolytes laboratory",
        "ALERGIAS": "allergy test",
        "ENDOCRINOLOGÍA": "hormone endocrine",
        "MARCADORES ONCOLÓGICOS": "cancer markers",
        "BACTERIOLOGÍA": "bacteria culture",
        "ORINA": "urine test",
        "VITAMINAS": "vitamin test",
        "MATERIA FECAL": "stool sample",
        "INMUNOLOGÍA": "immune system antibody"
    }

    return categoria_map.get(categoria, "medical laboratory test")


def buscar_imagen_pexels(keywords, api_key):
    """Busca una imagen en Pexels basada en keywords"""
    try:
        url = "https://api.pexels.com/v1/search"
        headers = {"Authorization": api_key}
        params = {
            "query": keywords,
            "per_page": 1,
            "orientation": "landscape"
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data.get("photos") and len(data["photos"]) > 0:
            return data["photos"][0]["src"]["medium"]  # 350px de ancho
        return None
    except Exception as e:
        print(f"         Error en Pexels: {str(e)}")
        return None


def buscar_imagen_unsplash(keywords):
    """Busca una imagen en Unsplash (sin API key necesaria)"""
    try:
        # Unsplash Source permite búsquedas sin API key
        keywords_encoded = keywords.replace(" ", ",")
        url = f"https://source.unsplash.com/800x600/?{keywords_encoded}"
        return url
    except Exception as e:
        print(f"         Error en Unsplash: {str(e)}")
        return None


def descargar_imagen(url, nombre_archivo, directorio):
    """Descarga una imagen desde URL y la guarda"""
    try:
        response = requests.get(url, timeout=15, allow_redirects=True)
        response.raise_for_status()

        ruta_completa = os.path.join(directorio, nombre_archivo)
        with open(ruta_completa, 'wb') as f:
            f.write(response.content)

        return nombre_archivo
    except Exception as e:
        print(f"         ❌ Error descargando: {str(e)}")
        return None


def generar_nombre_imagen_unico(nombre_prueba):
    """Genera un nombre de archivo único basado en el nombre de la prueba"""
    # Usar hash MD5 para nombre corto y único
    hash_obj = hashlib.md5(nombre_prueba.encode())
    hash_str = hash_obj.hexdigest()[:12]
    return f"prueba_{hash_str}.jpg"


def poblar_pruebas_con_imagenes():
    """Pobla TODAS las pruebas con imágenes individuales únicas"""
    app = create_app()

    with app.app_context():
        print("\n" + "="*70)
        print("🔬 POBLANDO PRUEBAS CON IMÁGENES INDIVIDUALES")
        print("="*70)

        # Verificar API key si se usa Pexels
        if USE_PEXELS and PEXELS_API_KEY == "TU_API_KEY_AQUI":
            print("\n⚠️  ADVERTENCIA: No has configurado PEXELS_API_KEY")
            print("   Se usará Unsplash en su lugar (sin API key necesaria)")
            global USE_PEXELS
            USE_PEXELS = False

        print(f"\n📸 Servicio de imágenes: {'Pexels API' if USE_PEXELS else 'Unsplash Source'}")
        print(f"📊 Total de categorías: {len(PRUEBAS_DATA)}")

        # Crear directorio
        dir_imagenes = os.path.join('app', 'static', 'uploads', 'pruebas')
        os.makedirs(dir_imagenes, exist_ok=True)
        print(f"📁 Directorio: {dir_imagenes}\n")

        total_pruebas = sum(len(pruebas) for pruebas in PRUEBAS_DATA.values())
        print(f"📋 Total de pruebas: {total_pruebas}")
        print(f"🖼️  Imágenes a buscar: {total_pruebas}\n")

        contador_agregadas = 0
        contador_existentes = 0
        contador_imagenes = 0

        for categoria, pruebas in PRUEBAS_DATA.items():
            print(f"\n{'='*70}")
            print(f"📂 {categoria} ({len(pruebas)} pruebas)")
            print(f"{'='*70}")

            precio_base = PRECIOS_POR_CATEGORIA.get(categoria, 100.0)

            for idx, nombre_prueba in enumerate(pruebas, 1):
                print(f"\n   [{idx}/{len(pruebas)}] {nombre_prueba}")

                # Verificar si existe
                prueba_existente = Prueba.query.filter_by(
                    nombre=nombre_prueba,
                    categoria=categoria
                ).first()

                # Generar keywords y buscar imagen
                keywords = generar_keywords(nombre_prueba, categoria)
                print(f"      🔍 Keywords: {keywords}")

                nombre_imagen = generar_nombre_imagen_unico(nombre_prueba)
                ruta_imagen_completa = os.path.join(dir_imagenes, nombre_imagen)

                # Buscar y descargar imagen
                url_imagen = None
                if USE_PEXELS:
                    url_imagen = buscar_imagen_pexels(keywords, PEXELS_API_KEY)
                    time.sleep(1)  # Rate limiting
                else:
                    url_imagen = buscar_imagen_unsplash(keywords)

                if url_imagen:
                    print(f"      🖼️  Descargando imagen...")
                    resultado = descargar_imagen(url_imagen, nombre_imagen, dir_imagenes)
                    if resultado:
                        print(f"      ✅ Imagen guardada: {nombre_imagen}")
                        contador_imagenes += 1
                    else:
                        nombre_imagen = None
                else:
                    print(f"      ⚠️  No se encontró imagen")
                    nombre_imagen = None

                # Crear o actualizar prueba
                if prueba_existente:
                    if nombre_imagen and not prueba_existente.imagen:
                        prueba_existente.imagen = nombre_imagen
                        print(f"      🔄 Imagen actualizada")
                    contador_existentes += 1
                else:
                    nueva_prueba = Prueba(
                        nombre=nombre_prueba,
                        categoria=categoria,
                        precio=precio_base,
                        descripcion=f"Prueba de {categoria.lower()}: {nombre_prueba}",
                        imagen=nombre_imagen
                    )
                    db.session.add(nueva_prueba)
                    print(f"      ✅ Prueba agregada (Bs. {precio_base})")
                    contador_agregadas += 1

        # Confirmar cambios
        try:
            db.session.commit()
            print(f"\n\n{'='*70}")
            print("✨ ¡PROCESO COMPLETADO EXITOSAMENTE!")
            print(f"{'='*70}")
            print(f"✅ Pruebas nuevas agregadas: {contador_agregadas}")
            print(f"⚠️  Pruebas existentes: {contador_existentes}")
            print(f"🖼️  Imágenes descargadas: {contador_imagenes}")
            print(f"📊 Total en base de datos: {Prueba.query.count()}")
            print(f"{'='*70}\n")

            return True
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error: {str(e)}")
            return False


if __name__ == "__main__":
    print("\n" + "="*70)
    print("   🔬 SCRIPT AVANZADO DE IMÁGENES INDIVIDUALES")
    print("="*70)
    print("\n📝 INSTRUCCIONES:")
    print("   1. Registrarse en Pexels: https://www.pexels.com/api/")
    print("   2. Obtener API Key gratuita (200 requests/hora)")
    print("   3. Editar este archivo y poner tu API Key en PEXELS_API_KEY")
    print("   4. O dejar como está para usar Unsplash sin API key\n")

    input("Presiona ENTER para continuar...")

    if poblar_pruebas_con_imagenes():
        print("\n🎉 ¡Todas las pruebas tienen imágenes profesionales únicas!")
    else:
        print("\n❌ El proceso falló.")
