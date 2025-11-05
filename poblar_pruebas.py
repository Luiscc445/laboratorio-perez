#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para poblar la base de datos con todas las pruebas de laboratorio
organizadas por categorías CON IMÁGENES PROFESIONALES
"""

import os
import requests
from app import create_app, db
from app.models import Prueba

# Datos de pruebas organizadas por categoría
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

# Precios sugeridos por categoría (en Bolivianos)
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

# IMÁGENES PROFESIONALES DE UNSPLASH POR CATEGORÍA
# Cada categoría tiene una imagen fija específica de alta calidad
IMAGENES_POR_CATEGORIA = {
    "HEMATOLOGÍA": "https://images.unsplash.com/photo-1631549916768-4119b2e5f926?w=800&h=600&fit=crop",  # Blood test tubes
    "COAGULACIÓN": "https://images.unsplash.com/photo-1579154204601-01588f351e67?w=800&h=600&fit=crop",  # Lab equipment
    "BIOQUÍMICA CLÍNICA": "https://images.unsplash.com/photo-1582719471137-c3967ffb1c42?w=800&h=600&fit=crop",  # Lab analysis
    "ELECTROLITOS": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&h=600&fit=crop",  # Chemical testing
    "ALERGIAS": "https://images.unsplash.com/photo-1576671081837-49000212a370?w=800&h=600&fit=crop",  # Allergy testing
    "ENDOCRINOLOGÍA": "https://images.unsplash.com/photo-1583912267550-bc83b8389e66?w=800&h=600&fit=crop",  # Hormone testing
    "MARCADORES ONCOLÓGICOS": "https://images.unsplash.com/photo-1530026405186-ed1f139313f8?w=800&h=600&fit=crop",  # Cancer research
    "BACTERIOLOGÍA": "https://images.unsplash.com/photo-1576086213369-97a306d36557?w=800&h=600&fit=crop",  # Petri dish bacteria
    "ORINA": "https://images.unsplash.com/photo-1584362917165-526a968579e8?w=800&h=600&fit=crop",  # Urine sample
    "VITAMINAS": "https://images.unsplash.com/photo-1550572017-edd951aa8f72?w=800&h=600&fit=crop",  # Vitamins
    "MATERIA FECAL": "https://images.unsplash.com/photo-1581595220892-b0739db3ba8c?w=800&h=600&fit=crop",  # Lab sample
    "PERFIL PRE-OPERATORIO": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=800&h=600&fit=crop",  # Surgery prep
    "PERFIL REUMATOIDEO": "https://images.unsplash.com/photo-1579154341141-a0c2c9e30b4e?w=800&h=600&fit=crop",  # Rheumatology
    "PERFIL HEPÁTICO": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&h=600&fit=crop",  # Liver tests
    "PERFIL OBSTÉTRICO CONTROL": "https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=800&h=600&fit=crop",  # Pregnancy test
    "MARCADORES DE HEPATITIS": "https://images.unsplash.com/photo-1584362917165-526a968579e8?w=800&h=600&fit=crop",  # Hepatitis testing
    "INMUNOLOGÍA": "https://images.unsplash.com/photo-1576086213369-97a306d36557?w=800&h=600&fit=crop",  # Immune system
    "PERFIL OBSTÉTRICO": "https://images.unsplash.com/photo-1631815589968-fdb09a223b1e?w=800&h=600&fit=crop",  # Obstetric care
    "BIOLOGÍA MOLECULAR": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&h=600&fit=crop"  # DNA/Molecular
}


def descargar_imagen(url, nombre_archivo, directorio):
    """Descarga una imagen desde una URL y la guarda localmente"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        ruta_completa = os.path.join(directorio, nombre_archivo)
        with open(ruta_completa, 'wb') as f:
            f.write(response.content)

        return nombre_archivo
    except Exception as e:
        print(f"      ❌ Error descargando imagen: {str(e)}")
        return None


def poblar_pruebas():
    """Pobla la base de datos con todas las pruebas de laboratorio CON IMÁGENES"""
    app = create_app()

    with app.app_context():
        print("🔬 Iniciando poblado de pruebas de laboratorio con imágenes...")
        print(f"📊 Total de categorías: {len(PRUEBAS_DATA)}")

        # Crear directorio de imágenes si no existe
        directorio_imagenes = os.path.join('app', 'static', 'uploads', 'pruebas')
        os.makedirs(directorio_imagenes, exist_ok=True)
        print(f"📁 Directorio de imágenes: {directorio_imagenes}")

        # Contar total de pruebas
        total_pruebas = sum(len(pruebas) for pruebas in PRUEBAS_DATA.values())
        print(f"📋 Total de pruebas a agregar: {total_pruebas}\n")

        contador_agregadas = 0
        contador_existentes = 0
        imagenes_descargadas = {}

        for categoria, pruebas in PRUEBAS_DATA.items():
            print(f"\n📂 Categoría: {categoria}")
            print(f"   Pruebas: {len(pruebas)}")

            precio_base = PRECIOS_POR_CATEGORIA.get(categoria, 100.0)
            url_imagen = IMAGENES_POR_CATEGORIA.get(categoria)

            # Descargar imagen de la categoría (una sola vez por categoría)
            nombre_imagen = None
            if url_imagen and categoria not in imagenes_descargadas:
                print(f"   🖼️  Descargando imagen para {categoria}...")
                nombre_imagen = f"{categoria.lower().replace(' ', '_')}.jpg"
                resultado = descargar_imagen(url_imagen, nombre_imagen, directorio_imagenes)
                if resultado:
                    imagenes_descargadas[categoria] = nombre_imagen
                    print(f"      ✅ Imagen descargada: {nombre_imagen}")
                else:
                    print(f"      ⚠️  No se pudo descargar imagen, se usará placeholder")
            elif categoria in imagenes_descargadas:
                nombre_imagen = imagenes_descargadas[categoria]

            for nombre_prueba in pruebas:
                # Verificar si la prueba ya existe
                prueba_existente = Prueba.query.filter_by(
                    nombre=nombre_prueba,
                    categoria=categoria
                ).first()

                if prueba_existente:
                    # Actualizar imagen si no tiene
                    if not prueba_existente.imagen and nombre_imagen:
                        prueba_existente.imagen = nombre_imagen
                        print(f"   🔄 Actualizada imagen: {nombre_prueba}")
                    else:
                        print(f"   ⚠️  Ya existe: {nombre_prueba}")
                    contador_existentes += 1
                else:
                    # Crear nueva prueba con imagen
                    nueva_prueba = Prueba(
                        nombre=nombre_prueba,
                        categoria=categoria,
                        precio=precio_base,
                        descripcion=f"Prueba de {categoria.lower()}: {nombre_prueba}",
                        imagen=nombre_imagen
                    )
                    db.session.add(nueva_prueba)
                    print(f"   ✅ Agregada: {nombre_prueba} (Bs. {precio_base}) + 🖼️")
                    contador_agregadas += 1

        # Confirmar cambios
        try:
            db.session.commit()
            print(f"\n{'='*60}")
            print("✨ ¡Poblado completado exitosamente!")
            print(f"{'='*60}")
            print(f"✅ Pruebas agregadas: {contador_agregadas}")
            print(f"⚠️  Pruebas que ya existían: {contador_existentes}")
            print(f"🖼️  Imágenes descargadas: {len(imagenes_descargadas)}")
            print(f"📊 Total en base de datos: {Prueba.query.count()}")
            print(f"{'='*60}\n")

            # Mostrar resumen por categoría
            print("\n📈 RESUMEN POR CATEGORÍA:")
            print(f"{'='*60}")
            for categoria in PRUEBAS_DATA.keys():
                cantidad = Prueba.query.filter_by(categoria=categoria).count()
                tiene_imagen = "🖼️" if categoria in imagenes_descargadas else "❌"
                print(f"   {categoria}: {cantidad} pruebas {tiene_imagen}")
            print(f"{'='*60}\n")

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error al guardar en la base de datos: {str(e)}")
            return False

        return True


if __name__ == "__main__":
    print("\n" + "="*60)
    print("   🔬 SCRIPT DE POBLADO DE PRUEBAS CON IMÁGENES")
    print("="*60 + "\n")

    if poblar_pruebas():
        print("🎉 Proceso completado con éxito!")
        print("\n💡 Todas las pruebas ahora tienen imágenes profesionales")
        print("   de alta calidad organizadas por categoría.")
    else:
        print("❌ El proceso falló. Revisa los errores anteriores.")
