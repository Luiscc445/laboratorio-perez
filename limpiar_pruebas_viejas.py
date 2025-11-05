"""
Script para eliminar pruebas viejas y mantener solo las del catálogo oficial
"""
from app import create_app, db
from app.models import Prueba

# Categorías válidas del catálogo oficial
CATEGORIAS_VALIDAS = [
    "HEMATOLOGÍA",
    "COAGULACIÓN",
    "BIOQUÍMICA CLÍNICA",
    "PERFIL HEPÁTICO",
    "PERFIL RENAL",
    "PERFIL LIPÍDICO",
    "ELECTROLITOS",
    "INMUNOLOGÍA",
    "HORMONAS",
    "MARCADORES TUMORALES",
    "MICROBIOLOGÍA",
    "PARASITOLOGÍA",
    "UROANÁLISIS",
    "SEROLOGÍA",
    "PRUEBAS ESPECIALES",
    "GASOMETRÍA",
    "PRUEBAS CARDIACAS",
    "VITAMINAS Y MINERALES",
    "ALERGIAS"
]

def limpiar_pruebas_viejas():
    app = create_app()
    with app.app_context():
        print("=" * 60)
        print("LIMPIANDO PRUEBAS VIEJAS DEL SISTEMA")
        print("=" * 60)

        # Obtener todas las pruebas
        todas_pruebas = Prueba.query.all()
        print(f"\n📊 Total de pruebas en el sistema: {len(todas_pruebas)}")

        # Identificar pruebas a eliminar (las que no están en categorías válidas)
        pruebas_a_eliminar = []

        for prueba in todas_pruebas:
            # Si la categoría no es válida o es None/vacía, marcar para eliminar
            if not prueba.categoria or prueba.categoria not in CATEGORIAS_VALIDAS:
                pruebas_a_eliminar.append(prueba)

        if not pruebas_a_eliminar:
            print("\n✅ No hay pruebas viejas para eliminar. Todo está limpio.")
            return

        print(f"\n🗑️  Pruebas a eliminar ({len(pruebas_a_eliminar)}):")
        print("-" * 60)

        for prueba in pruebas_a_eliminar:
            categoria = prueba.categoria or "Sin categoría"
            print(f"   • {prueba.nombre} (Categoría: {categoria})")

        print("\n" + "-" * 60)

        # Confirmar eliminación
        confirmacion = input("\n⚠️  ¿Deseas eliminar estas pruebas? (escribe 'SI' para confirmar): ")

        if confirmacion.upper() == "SI":
            eliminadas = 0
            for prueba in pruebas_a_eliminar:
                db.session.delete(prueba)
                eliminadas += 1

            db.session.commit()
            print(f"\n✅ Se eliminaron {eliminadas} pruebas viejas correctamente")

            # Mostrar resumen final
            pruebas_restantes = Prueba.query.all()
            print(f"📊 Pruebas restantes en el sistema: {len(pruebas_restantes)}")

            # Mostrar categorías actuales
            print("\n📂 Categorías actuales:")
            categorias = db.session.query(Prueba.categoria).distinct().filter(Prueba.categoria.isnot(None)).order_by(Prueba.categoria).all()
            for cat in categorias:
                if cat[0]:
                    count = Prueba.query.filter_by(categoria=cat[0]).count()
                    print(f"   • {cat[0]}: {count} pruebas")
        else:
            print("\n❌ Operación cancelada. No se eliminó ninguna prueba.")

if __name__ == '__main__':
    limpiar_pruebas_viejas()
