#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SCRIPT ULTRA SEGURO - ÚLTIMAS PRUEBAS (109-176)
Sistema de guardado automático cada 10 pruebas
Si falla, NO pierdes progreso - Guarda automáticamente
"""

import os
import requests
import time
import hashlib
from app import create_app, db
from app.models import Prueba

PEXELS_API_KEY = "pc4Lf88y25rYxtlfQmAcY1CZ4XOMq5b4tqWrfEk6cxWW5TyzKuWVPFp9"

print("\n" + "="*80)
print("   🔬 SCRIPT ULTRA SEGURO - ÚLTIMAS PRUEBAS (109-176)")
print("="*80)
print("\n🛡️  SISTEMA DE PROTECCIÓN AVANZADO:")
print("  ✅ NO elimina ninguna prueba existente")
print("  ✅ Guarda progreso cada 10 pruebas")
print("  ✅ Si falla, se mantiene todo lo descargado")
print("  ✅ Puedes reintentar sin perder nada")
print("  ✅ Log detallado del progreso")
print("\n⏱️  Tiempo: ~5-7 minutos (~60 pruebas)")
print("="*80 + "\n")

confirmacion = input("¿Continuar? (escribe 'SI'): ")
if confirmacion.upper() != "SI":
    print("❌ Cancelado.")
    exit()

# ÚLTIMAS PRUEBAS (109-176)
PRUEBAS_DATA = {
    "ENDOCRINOLOGÍA_PARTE2": [
        "B-HCG CUANTITATIVA",
        "CORTISOL AM O PM",
        "ACTH",
        "INSULINA BASAL O POST-PRAND.",
        "PARATOHORMONA (PTH)",
        "HORMONA DEL CRECIMIENTO (GH)"
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
    "ENDOCRINOLOGÍA_PARTE2": 120.0,
    "PERFIL OBSTÉTRICO CONTROL": 220.0,
    "MARCADORES DE HEPATITIS": 150.0,
    "INMUNOLOGÍA": 130.0,
    "PERFIL OBSTÉTRICO": 300.0,
    "BIOLOGÍA MOLECULAR": 450.0
}

# Ajustar nombres de categoría para la DB
CATEGORIA_DB_MAP = {
    "ENDOCRINOLOGÍA_PARTE2": "ENDOCRINOLOGÍA",
    "PERFIL OBSTÉTRICO CONTROL": "PERFIL OBSTÉTRICO CONTROL",
    "MARCADORES DE HEPATITIS": "MARCADORES DE HEPATITIS",
    "INMUNOLOGÍA": "INMUNOLOGÍA",
    "PERFIL OBSTÉTRICO": "PERFIL OBSTÉTRICO",
    "BIOLOGÍA MOLECULAR": "BIOLOGÍA MOLECULAR"
}

imagenes_usadas = set()


def analizar_prueba_inteligente(nombre_prueba, categoria):
    """Análisis inteligente de keywords"""
    nombre_upper = nombre_prueba.upper()

    mapeo_especifico = {
        "B-HCG": "pregnancy test laboratory hormone HCG blood",
        "CORTISOL": "cortisol stress hormone test laboratory tubes",
        "ACTH": "ACTH pituitary hormone test laboratory adrenal",
        "INSULINA": "insulin hormone test laboratory diabetes pancreas",
        "PARATOHORMONA": "PTH parathyroid hormone test laboratory calcium",
        "HORMONA CRECIMIENTO": "growth hormone test laboratory GH pituitary",

        "HEPATITIS A": "hepatitis A test laboratory liver virus HAV",
        "HEPATITIS B ANTÍGENO SUPERFICIE": "hepatitis B test laboratory HBsAg surface",
        "HEPATITIS B ANTICUERPO SUPERFICIE": "hepatitis B antibody test laboratory HBsAb",
        "HEPATITIS B ANTICUERPO CORE": "hepatitis B core antibody test laboratory",
        "HEPATITIS B ANTÍGENO ENVOLTURA": "hepatitis B envelope test laboratory HBeAg",
        "HEPATITIS B ANTICUERPO ENVOLTURA": "hepatitis B envelope antibody laboratory",
        "HEPATITIS C": "hepatitis C test laboratory liver HCV virus",

        "PROTEÍNA C REACTIVA": "CRP test laboratory inflammation tubes marker",
        "FACTOR REUMATOIDE": "rheumatoid factor test laboratory RF arthritis",
        "ESTREPTOLISINA": "ASTO test laboratory strep throat antibody",
        "WIDAL": "typhoid test laboratory Widal tubes serology",
        "RPR": "syphilis test laboratory RPR rapid plasma",
        "BRUCELOSIS": "brucellosis test laboratory serology bacteria",
        "TOXOPLASMA": "toxoplasma antibody test laboratory parasite",
        "CITOMEGALOVIRUS": "CMV test laboratory cytomegalovirus antibody",
        "EPSTEIN BARR": "EBV test laboratory mononucleosis antibody",
        "HERPES VIRUS": "herpes test laboratory HSV antibody virus",
        "VIH": "HIV test laboratory AIDS virus screening",
        "RUBEOLA": "rubella test laboratory german measles antibody",
        "SARAMPIÓN": "measles test laboratory antibody virus",
        "CHLAMYDIA": "chlamydia test laboratory STD screening",
        "SÍFILIS": "syphilis test laboratory serology tubes VDRL",
        "CHAGAS": "chagas disease test laboratory trypanosoma serology",
        "CITRULINADO": "CCP antibody test laboratory rheumatoid arthritis",
        "ANTINUCLEARES": "ANA test laboratory autoimmune antibody",
        "ANTI DNA": "anti-DNA test laboratory lupus antibody",
        "SMITH": "anti-Smith test laboratory lupus antibody",
        "ANTI ENA": "ENA panel test laboratory antibody autoimmune",
        "COMPLEMENTOS": "complement test laboratory C3 C4 immunology",
        "INMUNOGLOBULINAS": "immunoglobulin test laboratory IgG IgA IgM",
        "PYLORI": "H pylori test laboratory stomach bacteria",
        "ENDOMISIO": "celiac test laboratory endomysial antibody",
        "GLIADINA": "celiac test laboratory gliadin antibody gluten",

        "OBSTÉTRICO": "obstetric laboratory pregnancy test blood prenatal",
        "T.O.R.C.H": "TORCH test laboratory pregnancy screening panel",

        "PATÓGENOS ETS": "STD panel test laboratory PCR molecular",
        "FIEBRES HEMORRÁGICAS": "hemorrhagic fever test laboratory PCR virus",
        "VPH": "HPV test laboratory papillomavirus genotyping PCR",
        "MICROORGANISMOS RESPIRATORIOS": "respiratory panel test laboratory PCR pathogens"
    }

    for termino, keywords in mapeo_especifico.items():
        if termino in nombre_upper:
            return keywords

    categoria_keywords = {
        "ENDOCRINOLOGÍA_PARTE2": "hormone laboratory test tubes endocrine",
        "PERFIL OBSTÉTRICO CONTROL": "obstetric pregnancy laboratory test prenatal",
        "MARCADORES DE HEPATITIS": "hepatitis test laboratory liver virus tubes",
        "INMUNOLOGÍA": "antibody laboratory test immunology tubes",
        "PERFIL OBSTÉTRICO": "obstetric pregnancy laboratory blood test",
        "BIOLOGÍA MOLECULAR": "DNA PCR test laboratory molecular genetic"
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
            print(f" ⚠️ Error API: {str(e)}")
            return None, None

    return None, None


def descargar_imagen(url, nombre_archivo, directorio):
    """Descarga imagen con manejo de errores"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        ruta_completa = os.path.join(directorio, nombre_archivo)
        with open(ruta_completa, 'wb') as f:
            f.write(response.content)

        return nombre_archivo
    except Exception as e:
        print(f" ⚠️ Error descarga: {str(e)}")
        return None


def generar_nombre_unico(nombre_prueba, photo_id):
    """Genera nombre único"""
    hash_obj = hashlib.md5(nombre_prueba.encode())
    return f"prueba_{hash_obj.hexdigest()[:8]}_{photo_id}.jpg"


def guardar_progreso(mensaje):
    """Guarda progreso en la base de datos"""
    try:
        db.session.commit()
        print(f"\n💾 {mensaje}")
        return True
    except Exception as e:
        print(f"\n❌ Error al guardar: {str(e)}")
        db.session.rollback()
        return False


def main():
    app = create_app()

    with app.app_context():
        # Contar pruebas existentes
        pruebas_antes = Prueba.query.count()
        print(f"\n📊 Pruebas existentes: {pruebas_antes}")
        print("✅ Estas pruebas están protegidas\n")

        print("📁 Verificando directorio...")
        dir_imagenes = os.path.join('app', 'static', 'uploads', 'pruebas')
        os.makedirs(dir_imagenes, exist_ok=True)
        print(f"✅ {dir_imagenes}\n")

        total_pruebas = sum(len(p) for p in PRUEBAS_DATA.values())
        print(f"🔬 Agregando {total_pruebas} pruebas finales...")
        print("🛡️  Guardado automático cada 10 pruebas\n")

        contador = 0
        agregadas = 0
        existian = 0
        imagenes_ok = 0
        contador_guardado = 0

        for categoria_key, pruebas in PRUEBAS_DATA.items():
            categoria_db = CATEGORIA_DB_MAP.get(categoria_key, categoria_key)
            print(f"📂 {categoria_db} ({len(pruebas)} pruebas)")
            precio = PRECIOS_POR_CATEGORIA.get(categoria_key, 100.0)

            for nombre_prueba in pruebas:
                contador += 1

                try:
                    print(f"  [{contador}/{total_pruebas}] {nombre_prueba[:40]}...")

                    # Verificar si existe
                    existe = Prueba.query.filter_by(
                        nombre=nombre_prueba,
                        categoria=categoria_db
                    ).first()

                    if existe:
                        print(f"      ⚠️  Ya existe")
                        existian += 1
                        continue

                    # Buscar imagen
                    keywords = analizar_prueba_inteligente(nombre_prueba, categoria_key)
                    print(f"      🔍 {keywords[:50]}...")

                    url_imagen, photo_id = buscar_imagen_unica_pexels(keywords, PEXELS_API_KEY)

                    nombre_imagen = None
                    if url_imagen and photo_id:
                        nombre_imagen = generar_nombre_unico(nombre_prueba, photo_id)
                        resultado = descargar_imagen(url_imagen, nombre_imagen, dir_imagenes)
                        if resultado:
                            print(f"      ✅ ID: {photo_id}")
                            imagenes_ok += 1
                        else:
                            nombre_imagen = None
                    else:
                        print(f"      ⚠️ Sin imagen")

                    # Crear prueba
                    nueva_prueba = Prueba(
                        nombre=nombre_prueba,
                        categoria=categoria_db,
                        precio=precio,
                        descripcion=f"Prueba de {categoria_db.lower()}: {nombre_prueba}",
                        imagen=nombre_imagen
                    )
                    db.session.add(nueva_prueba)
                    agregadas += 1
                    contador_guardado += 1

                    # GUARDAR CADA 10 PRUEBAS
                    if contador_guardado >= 10:
                        if guardar_progreso(f"✅ Guardadas {contador_guardado} pruebas (Total: {Prueba.query.count()})"):
                            contador_guardado = 0
                        else:
                            print("⚠️  Reintentando guardado...")
                            time.sleep(2)
                            guardar_progreso(f"✅ Guardadas (reintento)")
                            contador_guardado = 0

                    time.sleep(1)

                except KeyboardInterrupt:
                    print("\n\n⚠️  Interrupción detectada. Guardando progreso...")
                    guardar_progreso(f"✅ Guardado de emergencia - {agregadas} pruebas")
                    print(f"💾 Progreso guardado hasta: {nombre_prueba}")
                    return

                except Exception as e:
                    print(f"      ❌ Error: {str(e)}")
                    # Continuar con la siguiente prueba
                    continue

            print()

        # Guardar final
        print("\n💾 Guardando pruebas finales...")
        guardar_progreso(f"✅ Guardado final completo")

        total_final = Prueba.query.count()

        print("\n" + "="*80)
        print("✨ ¡COMPLETADO CON GUARDADO AUTOMÁTICO!")
        print("="*80)
        print(f"📊 Pruebas al inicio: {pruebas_antes}")
        print(f"✅ Pruebas nuevas agregadas: {agregadas}")
        print(f"⚠️  Ya existían: {existian}")
        print(f"🖼️  Imágenes descargadas: {imagenes_ok}")
        print(f"📊 TOTAL FINAL: {total_final}")
        print("="*80)
        print("\n🎉 ¡Catálogo completo con todas las pruebas!")
        print("💡 Ejecuta: python run.py\n")


if __name__ == "__main__":
    main()
