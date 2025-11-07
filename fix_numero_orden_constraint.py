"""
Script para eliminar la restricción UNIQUE de numero_orden en Supabase
y permitir que un paciente tenga múltiples resultados.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# Conectar a Supabase
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL)

print("🔧 Actualizando restricciones de la tabla 'resultados' en Supabase...")
print("=" * 70)

try:
    with engine.connect() as conn:
        # 1. Verificar si existe la restricción unique
        result = conn.execute(text("""
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_name = 'resultados'
            AND constraint_type = 'UNIQUE'
            AND constraint_name LIKE '%numero_orden%';
        """))

        constraints = result.fetchall()

        if constraints:
            print(f"✓ Encontrada restricción UNIQUE: {constraints[0][0]}")

            # 2. Eliminar la restricción UNIQUE de numero_orden
            constraint_name = constraints[0][0]
            conn.execute(text(f"""
                ALTER TABLE resultados
                DROP CONSTRAINT IF EXISTS {constraint_name};
            """))
            conn.commit()
            print(f"✓ Restricción '{constraint_name}' eliminada exitosamente")
        else:
            print("ℹ No se encontró restricción UNIQUE en numero_orden (ya está correcto)")

        # 3. Agregar restricción UNIQUE a codigo_acceso si no existe
        result = conn.execute(text("""
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_name = 'resultados'
            AND constraint_type = 'UNIQUE'
            AND constraint_name LIKE '%codigo_acceso%';
        """))

        codigo_constraints = result.fetchall()

        if not codigo_constraints:
            print("➕ Agregando restricción UNIQUE a codigo_acceso...")
            conn.execute(text("""
                ALTER TABLE resultados
                ADD CONSTRAINT resultados_codigo_acceso_unique
                UNIQUE (codigo_acceso);
            """))
            conn.commit()
            print("✓ Restricción UNIQUE agregada a codigo_acceso")
        else:
            print("ℹ codigo_acceso ya tiene restricción UNIQUE")

        # 4. Verificar estado final
        print("\n📊 Estado final de la tabla 'resultados':")
        result = conn.execute(text("""
            SELECT
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = 'resultados'
            ORDER BY ordinal_position;
        """))

        for row in result:
            print(f"  - {row[0]}: {row[1]} (nullable={row[2]})")

        print("\n✅ Base de datos actualizada correctamente!")
        print("Ahora puedes subir múltiples resultados para el mismo paciente.")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print("\nSi el error persiste, ejecuta manualmente en Supabase SQL Editor:")
    print("""
    -- Eliminar restricción unique de numero_orden
    ALTER TABLE resultados DROP CONSTRAINT IF EXISTS resultados_numero_orden_key;

    -- Agregar restricción unique a codigo_acceso
    ALTER TABLE resultados ADD CONSTRAINT resultados_codigo_acceso_unique UNIQUE (codigo_acceso);
    """)
