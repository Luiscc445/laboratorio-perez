"""
Script para ejecutar desde Flask - Eliminar restricción UNIQUE de numero_orden
Ejecutar con: flask shell < fix_database.py
O copiar y pegar en flask shell
"""

from app import db
from sqlalchemy import text

print("🔧 Actualizando restricciones de la tabla 'resultados'...")
print("=" * 70)

try:
    # 1. Verificar si existe la restricción unique
    result = db.session.execute(text("""
        SELECT constraint_name
        FROM information_schema.table_constraints
        WHERE table_name = 'resultados'
        AND constraint_type = 'UNIQUE'
        AND constraint_name LIKE '%numero_orden%';
    """))

    constraints = result.fetchall()

    if constraints:
        constraint_name = constraints[0][0]
        print(f"✓ Encontrada restricción UNIQUE: {constraint_name}")

        # 2. Eliminar la restricción UNIQUE de numero_orden
        db.session.execute(text(f"""
            ALTER TABLE resultados
            DROP CONSTRAINT IF EXISTS {constraint_name};
        """))
        db.session.commit()
        print(f"✓ Restricción '{constraint_name}' eliminada exitosamente")
    else:
        print("ℹ No se encontró restricción UNIQUE en numero_orden (ya está correcto)")

    # 3. Agregar restricción UNIQUE a codigo_acceso si no existe
    result = db.session.execute(text("""
        SELECT constraint_name
        FROM information_schema.table_constraints
        WHERE table_name = 'resultados'
        AND constraint_type = 'UNIQUE'
        AND constraint_name LIKE '%codigo_acceso%';
    """))

    codigo_constraints = result.fetchall()

    if not codigo_constraints:
        print("➕ Agregando restricción UNIQUE a codigo_acceso...")
        db.session.execute(text("""
            ALTER TABLE resultados
            ADD CONSTRAINT resultados_codigo_acceso_unique
            UNIQUE (codigo_acceso);
        """))
        db.session.commit()
        print("✓ Restricción UNIQUE agregada a codigo_acceso")
    else:
        print("ℹ codigo_acceso ya tiene restricción UNIQUE")

    print("\n✅ Base de datos actualizada correctamente!")
    print("Ahora puedes subir múltiples resultados para el mismo paciente.")

except Exception as e:
    db.session.rollback()
    print(f"\n❌ Error: {str(e)}")
    print("\nEjecuta manualmente en Supabase SQL Editor:")
    print("""
    ALTER TABLE resultados DROP CONSTRAINT IF EXISTS resultados_numero_orden_key;
    ALTER TABLE resultados ADD CONSTRAINT resultados_codigo_acceso_unique UNIQUE (codigo_acceso);
    """)
