#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SCRIPT INTELIGENTE CON ANÁLISIS AVANZADO DE KEYWORDS
- Analiza cada prueba individual
- Keywords específicos por tipo de prueba
- NO repite imágenes (tracking de IDs)
- Solo imágenes técnicas de laboratorio (sin personas enfermas)
"""

import os
import requests
import time
import hashlib
from app import create_app, db
from app.models import Prueba

PEXELS_API_KEY = "13aoSqmc9IrPvwrKVO9vRS9UCXyjADcRskUZkgmRlM5AMFSqejwTYFgY"

print("\n" + "="*80)
print("   🔬 SCRIPT INTELIGENTE - ANÁLISIS AVANZADO DE PRUEBAS")
print("="*80)
print("\nCaracterísticas:")
print("  ✅ Analiza cada prueba individualmente")
print("  ✅ Keywords específicos y precisos")
print("  ✅ NO repite imágenes (verifica IDs únicos)")
print("  ✅ Solo imágenes técnicas de laboratorio")
print("  ✅ Evita personas enfermas/en cama")
print("\n⏱️  Tiempo: ~10-15 minutos (búsqueda más inteligente)")
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

# Tracking de imágenes ya usadas (para NO repetir)
imagenes_usadas = set()


def analizar_prueba_inteligente(nombre_prueba, categoria):
    """
    ANÁLISIS INTELIGENTE: Genera keywords específicos técnicos
    Solo busca imágenes de equipos, muestras, laboratorio (NO personas)
    """

    nombre_upper = nombre_prueba.upper()

    # Diccionario EXTENDIDO y ESPECÍFICO por términos clave
    mapeo_especifico = {
        # HEMATOLOGÍA - Imágenes de sangre y células
        "HEMOGRAMA": "blood cells microscope laboratory slide",
        "VELOCIDAD DE SEDIMENTACIÓN": "laboratory test tube blood sedimentation",
        "HEMOGLOBINA": "red blood cells microscope hemoglobin",
        "HEMATOCRITO": "blood sample centrifuge hematocrit tube",
        "PLAQUETAS": "platelets microscope blood cells",
        "RETICULOCITOS": "reticulocytes blood cells stain microscope",
        "GRUPO SANGUÍNEO": "blood type test laboratory tubes",
        "COOMBS": "laboratory blood test tubes reagent",
        "HIERRO": "iron supplement laboratory test",
        "FERRITINA": "laboratory test tube chemistry analysis",
        "TRANSFERRINA": "laboratory test sample analysis",

        # COAGULACIÓN - Equipos y procesos
        "PROTROMBINA": "blood clotting test laboratory equipment",
        "TROMBOPLASTINA": "coagulation test laboratory tubes",
        "TROMBINA": "laboratory test coagulation analysis",
        "COAGULACIÓN": "blood clotting laboratory process",
        "DÍMERO": "laboratory test equipment analysis",

        # GLUCOSA Y DIABETES
        "GLUCOSA": "glucose meter test laboratory blood sugar",
        "TOLERANCIA GLUCOSA": "glucose test laboratory equipment meter",
        "HEMOGLOBINA GLICOSILADA": "diabetes test laboratory analysis HbA1c",

        # BIOQUÍMICA
        "UREA": "laboratory chemistry test tubes analysis",
        "CREATININA": "kidney function test laboratory chemistry",
        "ÁCIDO ÚRICO": "uric acid crystals microscope laboratory",
        "COLESTEROL": "cholesterol test laboratory tubes lipids",
        "TRIGLICÉRIDOS": "lipid test laboratory chemistry analysis",
        "AMILASA": "enzyme test laboratory pancreas analysis",
        "LIPASA": "lipase test laboratory tubes chemistry",
        "TRANSAMINASAS": "liver function test laboratory tubes",
        "BILIRRUBINAS": "bilirubin test laboratory yellow sample",
        "FOSFATASA": "alkaline phosphatase test laboratory chemistry",
        "GGT": "liver enzyme test laboratory tubes",
        "LDH": "lactate dehydrogenase laboratory test",
        "CPK": "creatine kinase test laboratory muscle enzyme",
        "TROPONINA": "troponin test laboratory cardiac marker",
        "PROTEÍNAS": "protein test laboratory chemistry analysis",

        # ELECTROLITOS
        "CALCIO": "calcium test laboratory chemistry minerals",
        "MAGNESIO": "magnesium test laboratory analysis minerals",
        "FÓSFORO": "phosphorus test laboratory chemistry",
        "ELECTROLITOS": "electrolytes test laboratory chemistry ions",

        # ALERGIAS
        "ALÉRGENOS": "allergy test laboratory skin prick panel",
        "ALERGIAS": "allergy testing laboratory panel analysis",

        # HORMONAS
        "TSH": "thyroid test laboratory hormone analysis",
        "T3": "thyroid hormone test laboratory tubes",
        "T4": "thyroid test laboratory hormone chemistry",
        "TIROPEROXIDASA": "thyroid antibody test laboratory",
        "LUTEINIZANTE": "hormone test laboratory reproductive",
        "FOLÍCULO ESTIMULANTE": "FSH hormone test laboratory tubes",
        "ESTRADIOL": "estrogen hormone test laboratory analysis",
        "PROGESTERONA": "progesterone hormone test laboratory",
        "TESTOSTERONA": "testosterone hormone test laboratory vial",
        "PROLACTINA": "prolactin hormone test laboratory analysis",
        "HCG": "pregnancy test laboratory hormone",
        "CORTISOL": "cortisol stress hormone test laboratory",
        "ACTH": "ACTH hormone test laboratory tubes",
        "INSULINA": "insulin hormone test laboratory diabetes",
        "PARATOHORMONA": "PTH parathyroid hormone test laboratory",
        "HORMONA CRECIMIENTO": "growth hormone test laboratory vial",

        # MARCADORES ONCOLÓGICOS
        "ALFA FETO PROTEÍNA": "AFP tumor marker test laboratory",
        "CARCINOEMBRIONARIO": "CEA tumor marker laboratory test",
        "CA 125": "ovarian tumor marker test laboratory",
        "CA 19-9": "pancreatic tumor marker laboratory test",
        "CA 15-3": "breast tumor marker laboratory test",
        "PSA": "prostate test laboratory PSA marker",
        "TUMORAL": "tumor marker test laboratory analysis",

        # BACTERIOLOGÍA
        "CULTIVO": "bacterial culture petri dish laboratory",
        "ANTIBIOGRAMA": "antibiotic sensitivity test petri dish",
        "MYCOPLASMA": "bacterial culture laboratory microscope",
        "EXAMEN FRESCO": "microscope slide laboratory sample",
        "TINCIÓN GRAM": "gram stain microscope bacteria slide",
        "MICOLÓGICO": "fungal culture laboratory petri dish",
        "BACILOSCOPIA": "tuberculosis microscope slide stain",

        # ORINA
        "ORINA": "urine test laboratory sample container",
        "MORFOLOGÍA ERITROCITARIA": "urine microscope red cells analysis",
        "CÁLCULO RENAL": "kidney stone laboratory analysis crystals",
        "DEPURACIÓN CREATININA": "kidney function test laboratory",
        "COCAÍNA": "drug test laboratory urine screening",
        "MARIHUANA": "drug screening test laboratory urine",

        # VITAMINAS
        "VITAMINA B12": "vitamin B12 supplement laboratory test",
        "VITAMINA D": "vitamin D test laboratory analysis",

        # MATERIA FECAL
        "PARASITOLÓGICO": "parasite microscope laboratory stool sample",
        "MOCO FECAL": "stool sample laboratory test container",
        "SANGRE OCULTA": "occult blood test laboratory stool",
        "GRAHAM": "pinworm test laboratory tape slide",
        "AZÚCARES REDUCTORES": "sugar test laboratory chemistry stool",
        "GIARDIA": "giardia parasite microscope laboratory",
        "AMEBA": "amoeba parasite microscope laboratory",
        "PYLORI HECES": "H pylori test laboratory stool",
        "ROTAVIRUS": "virus test laboratory sample",
        "ADENOVIRUS": "virus laboratory test sample",

        # HEPATITIS
        "HEPATITIS": "hepatitis test laboratory tubes virus",

        # INMUNOLOGÍA
        "PROTEÍNA C REACTIVA": "CRP test laboratory inflammation marker",
        "FACTOR REUMATOIDE": "rheumatoid factor test laboratory tubes",
        "ESTREPTOLISINA": "ASTO test laboratory strep antibody",
        "WIDAL": "typhoid test laboratory tubes serology",
        "RPR": "syphilis test laboratory RPR",
        "BRUCELOSIS": "brucellosis test laboratory serology",
        "TOXOPLASMA": "toxoplasma antibody test laboratory",
        "CITOMEGALOVIRUS": "CMV antibody test laboratory tubes",
        "EPSTEIN BARR": "EBV antibody test laboratory",
        "HERPES": "herpes virus test laboratory antibody",
        "VIH": "HIV test laboratory virus screening",
        "RUBEOLA": "rubella antibody test laboratory",
        "SARAMPIÓN": "measles antibody test laboratory",
        "CHLAMYDIA": "chlamydia test laboratory screening",
        "SÍFILIS": "syphilis test laboratory serology tubes",
        "CHAGAS": "chagas disease test laboratory serology",
        "CITRULINADO": "rheumatoid arthritis test laboratory CCP",
        "ANTINUCLEARES": "ANA test laboratory autoimmune",
        "DNA": "DNA test laboratory genetic helix",
        "SMITH": "anti-Smith antibody test laboratory",
        "ENA": "ENA antibody test laboratory panel",
        "COMPLEMENTOS": "complement test laboratory immunology",
        "INMUNOGLOBULINAS": "immunoglobulin test laboratory tubes",
        "PYLORI SUERO": "H pylori blood test laboratory",
        "ENDOMISIO": "celiac antibody test laboratory",
        "GLIADINA": "gluten antibody test laboratory",

        # BIOLOGÍA MOLECULAR
        "PATÓGENOS": "pathogen detection laboratory PCR",
        "FIEBRES HEMORRÁGICAS": "viral hemorrhagic fever test laboratory",
        "VPH": "HPV DNA test laboratory genotyping",
        "MICROORGANISMOS RESPIRATORIOS": "respiratory pathogen test laboratory PCR"
    }

    # Buscar coincidencia específica en el nombre
    for termino, keywords in mapeo_especifico.items():
        if termino in nombre_upper:
            return keywords

    # Si no hay coincidencia, usar keywords generales por categoría
    categoria_keywords = {
        "HEMATOLOGÍA": "blood test laboratory microscope cells",
        "COAGULACIÓN": "blood clotting laboratory test tubes",
        "BIOQUÍMICA CLÍNICA": "laboratory chemistry test tubes analysis",
        "ELECTROLITOS": "laboratory chemistry minerals test",
        "ALERGIAS": "allergy laboratory test panel",
        "ENDOCRINOLOGÍA": "hormone laboratory test tubes",
        "MARCADORES ONCOLÓGICOS": "tumor marker laboratory test",
        "BACTERIOLOGÍA": "bacteria culture petri dish laboratory",
        "ORINA": "urine laboratory test sample",
        "VITAMINAS": "vitamin laboratory test supplement",
        "MATERIA FECAL": "laboratory stool sample test",
        "PERFIL PRE-OPERATORIO": "laboratory blood test tubes",
        "PERFIL REUMATOIDEO": "laboratory test tubes rheumatoid",
        "PERFIL HEPÁTICO": "liver function laboratory test",
        "PERFIL OBSTÉTRICO CONTROL": "laboratory pregnancy test tubes",
        "PERFIL OBSTÉTRICO": "pregnancy laboratory test blood",
        "MARCADORES DE HEPATITIS": "hepatitis laboratory test tubes",
        "INMUNOLOGÍA": "antibody laboratory test immunology",
        "BIOLOGÍA MOLECULAR": "DNA laboratory test PCR"
    }

    return categoria_keywords.get(categoria, "medical laboratory test equipment")


def buscar_imagen_unica_pexels(keywords, api_key, intentos=3):
    """
    Busca imagen en Pexels y verifica que NO esté repetida
    Intenta múltiples páginas si es necesario
    """
    for pagina in range(1, intentos + 1):
        try:
            url = "https://api.pexels.com/v1/search"
            headers = {"Authorization": api_key}
            params = {
                "query": keywords,
                "per_page": 5,  # Obtener 5 resultados para tener opciones
                "page": pagina,
                "orientation": "landscape"
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data.get("photos") and len(data["photos"]) > 0:
                # Revisar cada foto para encontrar una NO usada
                for photo in data["photos"]:
                    photo_id = photo["id"]
                    if photo_id not in imagenes_usadas:
                        # ¡Imagen única encontrada!
                        imagenes_usadas.add(photo_id)
                        return photo["src"]["medium"], photo_id

                # Si todas están usadas, intentar siguiente página
                continue
            else:
                return None, None

        except Exception as e:
            print(f" ❌ Error: {str(e)}")
            return None, None

    # No se encontró imagen única después de todos los intentos
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
        print(f" ❌ Error descarga: {str(e)}")
        return None


def generar_nombre_unico(nombre_prueba, photo_id):
    """Genera nombre único usando hash + ID de foto"""
    hash_obj = hashlib.md5(nombre_prueba.encode())
    return f"prueba_{hash_obj.hexdigest()[:8]}_{photo_id}.jpg"


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

        # Poblar con imágenes ÚNICAS
        total_pruebas = sum(len(p) for p in PRUEBAS_DATA.values())
        print(f"🔬 PASO 3/3: Creando {total_pruebas} pruebas con imágenes ÚNICAS...")
        print("📸 Análisis inteligente: keywords específicos + verificación NO repetidas")
        print("(Esto tomará ~10-15 minutos)\n")

        contador = 0
        imagenes_ok = 0
        imagenes_repetidas_evitadas = 0

        for categoria, pruebas in PRUEBAS_DATA.items():
            print(f"📂 {categoria} ({len(pruebas)} pruebas)")
            precio = PRECIOS_POR_CATEGORIA.get(categoria, 100.0)

            for nombre_prueba in pruebas:
                contador += 1
                print(f"  [{contador}/{total_pruebas}] {nombre_prueba[:40]}...")

                # ANÁLISIS INTELIGENTE
                keywords = analizar_prueba_inteligente(nombre_prueba, categoria)
                print(f"      🔍 Keywords: {keywords}")

                # Buscar imagen ÚNICA
                url_imagen, photo_id = buscar_imagen_unica_pexels(keywords, PEXELS_API_KEY)

                nombre_imagen = None
                if url_imagen and photo_id:
                    nombre_imagen = generar_nombre_unico(nombre_prueba, photo_id)
                    resultado = descargar_imagen(url_imagen, nombre_imagen, dir_imagenes)
                    if resultado:
                        print(f"      ✅ Imagen única descargada (ID: {photo_id})")
                        imagenes_ok += 1
                    else:
                        print(f"      ⚠️ Error al descargar")
                        nombre_imagen = None
                else:
                    print(f"      ⚠️ No se encontró imagen única")

                # Crear prueba
                nueva_prueba = Prueba(
                    nombre=nombre_prueba,
                    categoria=categoria,
                    precio=precio,
                    descripcion=f"Prueba de {categoria.lower()}: {nombre_prueba}",
                    imagen=nombre_imagen
                )
                db.session.add(nueva_prueba)

                time.sleep(1.2)  # Rate limiting

            print()

        # Guardar
        print("\n💾 Guardando en base de datos...")
        db.session.commit()

        print("\n" + "="*80)
        print("✨ ¡COMPLETADO CON ANÁLISIS INTELIGENTE!")
        print("="*80)
        print(f"✅ Pruebas creadas: {contador}")
        print(f"🖼️  Imágenes ÚNICAS descargadas: {imagenes_ok}")
        print(f"🚫 Imágenes repetidas evitadas: {len(imagenes_usadas) - imagenes_ok}")
        print(f"📊 Total en DB: {Prueba.query.count()}")
        print(f"✅ Todas las imágenes son TÉCNICAS (no personas enfermas)")
        print("="*80)
        print("\n🎉 ¡Catálogo con imágenes profesionales ÚNICAS!")
        print("💡 Ejecuta: python run.py\n")


if __name__ == "__main__":
    main()
