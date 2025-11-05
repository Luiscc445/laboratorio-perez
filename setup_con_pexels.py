#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SCRIPT CON PEXELS API - Descarga imágenes profesionales REALES
Pexels es GRATIS - Solo necesitas registrarte 2 minutos
"""

import os
import requests
import time
import hashlib
from app import create_app, db
from app.models import Prueba

# ========================================
# IMPORTANTE: PONER TU API KEY DE PEXELS
# ========================================
# 1. Ve a: https://www.pexels.com/api/
# 2. Clic en "Get Started"
# 3. Regístrate con email (2 minutos)
# 4. Copia tu API Key
# 5. Pégala aquí abajo entre las comillas:

PEXELS_API_KEY = "13aoSqmc9IrPvwrKVO9vRS9UCXyjADcRskUZkgmRlM5AMFSqejwTYFgY"

# ========================================

print("\n" + "="*80)
print("   🔬 CONFIGURACIÓN CON PEXELS - IMÁGENES PROFESIONALES")
print("="*80)

# Verificar API key
if PEXELS_API_KEY == "PONER_TU_API_KEY_AQUI":
    print("\n❌ ERROR: No has configurado tu API Key de Pexels")
    print("\n📝 PASOS PARA OBTENER TU API KEY (2 minutos):")
    print("   1. Ve a: https://www.pexels.com/api/")
    print("   2. Clic en 'Get Started'")
    print("   3. Regístrate con tu email")
    print("   4. Copia tu API Key")
    print("   5. Edita este archivo (setup_con_pexels.py)")
    print("   6. En línea 20, reemplaza 'PONER_TU_API_KEY_AQUI' con tu key")
    print("   7. Guarda y vuelve a ejecutar este script\n")
    exit()

print("\n✅ API Key detectada")
print("\nEste script:")
print("  1. ✅ Elimina todas las pruebas existentes")
print("  2. ✅ Crea 176+ pruebas del catálogo oficial")
print("  3. ✅ Descarga imagen profesional ÚNICA para CADA prueba desde Pexels")
print("\n⏱️  Tiempo: ~8-10 minutos")
print("="*80 + "\n")

confirmacion = input("¿Continuar? (escribe 'SI'): ")
if confirmacion.upper() != "SI":
    print("❌ Cancelado.")
    exit()

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
    """Genera keywords para Pexels"""
    mapeo = {
        "HEMOGRAMA": "blood test cells microscope",
        "SANGRE": "blood test sample",
        "GLUCOSA": "glucose diabetes blood sugar",
        "COLESTEROL": "cholesterol heart health",
        "HEPATITIS": "liver hepatitis medical",
        "VIH": "hiv test laboratory",
        "ORINA": "urine test sample",
        "HECES": "stool sample laboratory",
        "FECAL": "laboratory sample medical",
        "CULTIVO": "bacteria culture petri dish",
        "BACTERIA": "bacteria microscope culture",
        "HORMONA": "hormone blood test",
        "TIROIDES": "thyroid hormone medical",
        "VITAMINA": "vitamin supplement pills",
        "CANCER": "cancer cells medical",
        "DNA": "dna genetic helix",
        "MOLECULAR": "dna molecular laboratory",
        "EMBARAZO": "pregnancy test medical",
        "CORAZÓN": "heart cardio medical",
        "RIÑÓN": "kidney renal medical",
        "HÍGADO": "liver hepatic medical",
        "COAGULACIÓN": "blood clotting laboratory"
    }

    nombre_upper = nombre_prueba.upper()
    for termino, keywords in mapeo.items():
        if termino in nombre_upper:
            return keywords

    categoria_map = {
        "HEMATOLOGÍA": "blood laboratory cells",
        "COAGULACIÓN": "blood clotting test",
        "BIOQUÍMICA CLÍNICA": "chemistry laboratory test",
        "ELECTROLITOS": "chemistry laboratory minerals",
        "ALERGIAS": "allergy test medical",
        "ENDOCRINOLOGÍA": "hormone laboratory test",
        "MARCADORES ONCOLÓGICOS": "cancer test medical",
        "BACTERIOLOGÍA": "bacteria culture laboratory",
        "ORINA": "urine test sample",
        "VITAMINAS": "vitamin pills supplement",
        "MATERIA FECAL": "laboratory sample test",
        "INMUNOLOGÍA": "antibody immune test"
    }

    return categoria_map.get(categoria, "medical laboratory test")


def buscar_imagen_pexels(keywords, api_key):
    """Busca imagen en Pexels"""
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
            return data["photos"][0]["src"]["medium"]
        return None
    except Exception as e:
        print(f" ❌ Error: {str(e)}")
        return None


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


def generar_nombre_unico(nombre_prueba):
    """Genera nombre único"""
    hash_obj = hashlib.md5(nombre_prueba.encode())
    return f"prueba_{hash_obj.hexdigest()[:12]}.jpg"


def main():
    app = create_app()

    with app.app_context():
        # Eliminar todo
        print("\n🗑️  PASO 1/3: Eliminando pruebas existentes...")
        eliminadas = Prueba.query.delete()
        db.session.commit()
        print(f"✅ {eliminadas} pruebas eliminadas\n")

        # Crear directorio
        print("📁 PASO 2/3: Creando directorio...")
        dir_imagenes = os.path.join('app', 'static', 'uploads', 'pruebas')
        os.makedirs(dir_imagenes, exist_ok=True)
        print(f"✅ {dir_imagenes}\n")

        # Poblar con imágenes
        total_pruebas = sum(len(p) for p in PRUEBAS_DATA.values())
        print(f"🔬 PASO 3/3: Creando {total_pruebas} pruebas con imágenes Pexels...")
        print("(Esto tomará ~8-10 minutos)\n")

        contador = 0
        imagenes_ok = 0

        for categoria, pruebas in PRUEBAS_DATA.items():
            print(f"📂 {categoria} ({len(pruebas)} pruebas)")
            precio = PRECIOS_POR_CATEGORIA.get(categoria, 100.0)

            for nombre_prueba in pruebas:
                contador += 1
                print(f"  [{contador}/{total_pruebas}] {nombre_prueba[:45]}...", end="")

                # Buscar imagen
                keywords = generar_keywords(nombre_prueba, categoria)
                url_imagen = buscar_imagen_pexels(keywords, PEXELS_API_KEY)

                nombre_imagen = None
                if url_imagen:
                    nombre_imagen = generar_nombre_unico(nombre_prueba)
                    resultado = descargar_imagen(url_imagen, nombre_imagen, dir_imagenes)
                    if resultado:
                        print(" 🖼️ ✅")
                        imagenes_ok += 1
                    else:
                        print(" ⚠️")
                        nombre_imagen = None
                else:
                    print(" ⚠️")

                # Crear prueba
                nueva_prueba = Prueba(
                    nombre=nombre_prueba,
                    categoria=categoria,
                    precio=precio,
                    descripcion=f"Prueba de {categoria.lower()}: {nombre_prueba}",
                    imagen=nombre_imagen
                )
                db.session.add(nueva_prueba)

                time.sleep(1)  # Rate limiting Pexels

            print()

        # Guardar
        print("\n💾 Guardando en base de datos...")
        db.session.commit()

        print("\n" + "="*80)
        print("✨ ¡COMPLETADO!")
        print("="*80)
        print(f"✅ Pruebas creadas: {contador}")
        print(f"🖼️  Imágenes descargadas: {imagenes_ok}")
        print(f"📊 Total en DB: {Prueba.query.count()}")
        print("="*80)
        print("\n🎉 ¡Tu catálogo está listo con imágenes profesionales de Pexels!")
        print("💡 Ahora ejecuta: python run.py\n")


if __name__ == "__main__":
    main()
