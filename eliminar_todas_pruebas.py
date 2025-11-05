"""
Script para ELIMINAR TODAS LAS PRUEBAS de la base de datos
ADVERTENCIA: Esta acción es irreversible y borrará todo el catálogo
"""
from app import create_app, db
from app.models import Prueba

def eliminar_todas_las_pruebas():
    app = create_app()
    with app.app_context():
        print("=" * 70)
        print("⚠️  ADVERTENCIA: ELIMINACIÓN TOTAL DE PRUEBAS ⚠️")
        print("=" * 70)

        # Contar pruebas actuales
        total_pruebas = Prueba.query.count()

        if total_pruebas == 0:
            print("\n✅ No hay pruebas en la base de datos. Ya está limpia.")
            return

        print(f"\n📊 Total de pruebas en el sistema: {total_pruebas}")

        # Mostrar categorías y conteo
        print("\n📂 Distribución por categorías:")
        print("-" * 70)

        categorias = db.session.query(Prueba.categoria, db.func.count(Prueba.id))\
            .group_by(Prueba.categoria)\
            .order_by(Prueba.categoria)\
            .all()

        for cat, count in categorias:
            categoria_nombre = cat if cat else "Sin categoría"
            print(f"   • {categoria_nombre}: {count} pruebas")

        print("\n" + "-" * 70)
        print("⚠️  ESTA ACCIÓN ELIMINARÁ TODAS LAS PRUEBAS DE LA BASE DE DATOS")
        print("⚠️  NO SE PUEDE DESHACER - TODOS LOS DATOS SE PERDERÁN")
        print("-" * 70)

        # Confirmación doble
        confirmacion1 = input("\n¿Estás SEGURO que deseas eliminar TODAS las pruebas? (escribe 'SI' para continuar): ")

        if confirmacion1.upper() != "SI":
            print("\n❌ Operación cancelada. No se eliminó ninguna prueba.")
            return

        confirmacion2 = input("\n⚠️  ÚLTIMA CONFIRMACIÓN - Escribe 'ELIMINAR TODO' para proceder: ")

        if confirmacion2.upper() != "ELIMINAR TODO":
            print("\n❌ Operación cancelada. No se eliminó ninguna prueba.")
            return

        print("\n🗑️  Eliminando todas las pruebas...")

        try:
            # Eliminar todas las pruebas
            eliminadas = Prueba.query.delete()
            db.session.commit()

            print(f"\n✅ ¡Completado! Se eliminaron {eliminadas} pruebas de la base de datos")
            print("📊 Pruebas restantes: 0")
            print("\n💡 Ahora puedes ejecutar 'python poblar_pruebas.py' para agregar el catálogo oficial")

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error al eliminar pruebas: {e}")

if __name__ == '__main__':
    eliminar_todas_las_pruebas()
