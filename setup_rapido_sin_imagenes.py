#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SCRIPT RÁPIDO - Crea todas las pruebas SIN imágenes
Después puedes agregar imágenes desde el panel admin si quieres
"""

from app import create_app, db
from app.models import Prueba

print("\n" + "="*80)
print("   🔬 CONFIGURACIÓN RÁPIDA - SIN DESCARGAR IMÁGENES")
print("="*80)
print("\nEste script:")
print("  1. ✅ Elimina todas las pruebas existentes")
print("  2. ✅ Crea 176+ pruebas del catálogo oficial")
print("  3. ⏩ Sin descargar imágenes (más rápido)")
print("\n⏱️  Tiempo: ~5 segundos")
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

def main():
    app = create_app()

    with app.app_context():
        print("\n🗑️  Eliminando pruebas existentes...")
        eliminadas = Prueba.query.delete()
        db.session.commit()
        print(f"✅ {eliminadas} pruebas eliminadas\n")

        print("🔬 Creando pruebas nuevas...\n")

        contador = 0
        for categoria, pruebas in PRUEBAS_DATA.items():
            precio = PRECIOS_POR_CATEGORIA.get(categoria, 100.0)

            for nombre_prueba in pruebas:
                nueva_prueba = Prueba(
                    nombre=nombre_prueba,
                    categoria=categoria,
                    precio=precio,
                    descripcion=f"Prueba de {categoria.lower()}: {nombre_prueba}",
                    imagen=None
                )
                db.session.add(nueva_prueba)
                contador += 1

            print(f"  ✅ {categoria}: {len(pruebas)} pruebas")

        db.session.commit()

        print("\n" + "="*80)
        print("✨ ¡COMPLETADO!")
        print("="*80)
        print(f"✅ Pruebas creadas: {contador}")
        print(f"📊 Total en DB: {Prueba.query.count()}")
        print("="*80)
        print("\n💡 Ahora ejecuta: python run.py")
        print("📸 Las pruebas NO tienen imágenes (usarán placeholder)")
        print("   Puedes agregar imágenes después desde el panel admin\n")

if __name__ == "__main__":
    main()
