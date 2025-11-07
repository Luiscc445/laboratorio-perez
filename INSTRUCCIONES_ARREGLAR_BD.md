# 🔧 INSTRUCCIONES PARA ARREGLAR LA BASE DE DATOS

## Problema
El campo `numero_orden` tiene una restricción UNIQUE que impide subir múltiples resultados. Esto causa el error:
```
duplicate key value violates unique constraint "resultados_numero_orden_key"
```

## Solución

### Opción 1: Ejecutar en Supabase SQL Editor (RECOMENDADO)

1. **Ir a Supabase Dashboard**
   - https://supabase.com/dashboard
   - Selecciona tu proyecto

2. **Abrir SQL Editor**
   - En el menú lateral, click en "SQL Editor"
   - Click en "New Query"

3. **Copiar y pegar este SQL:**

```sql
-- 1. Eliminar restricción UNIQUE de numero_orden
ALTER TABLE resultados
DROP CONSTRAINT IF EXISTS resultados_numero_orden_key;

-- 2. Agregar restricción UNIQUE a codigo_acceso
ALTER TABLE resultados
ADD CONSTRAINT resultados_codigo_acceso_unique
UNIQUE (codigo_acceso);

-- 3. Verificar cambios
SELECT
    constraint_name,
    constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'resultados'
ORDER BY constraint_name;
```

4. **Ejecutar el SQL** (botón RUN o Ctrl+Enter)

5. **Verificar resultado**
   - Deberías ver un mensaje de éxito
   - Ya NO debe aparecer `resultados_numero_orden_key`
   - DEBE aparecer `resultados_codigo_acceso_unique`

---

### Opción 2: Desde la aplicación Flask

Si prefieres ejecutar desde Python:

```bash
# En tu terminal (Windows)
python
```

```python
from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    # Eliminar restricción
    db.session.execute(text("""
        ALTER TABLE resultados
        DROP CONSTRAINT IF EXISTS resultados_numero_orden_key;
    """))

    # Agregar nueva restricción
    db.session.execute(text("""
        ALTER TABLE resultados
        ADD CONSTRAINT resultados_codigo_acceso_unique
        UNIQUE (codigo_acceso);
    """))

    db.session.commit()
    print("✅ Base de datos actualizada!")
```

---

## ✅ Verificación

Después de ejecutar los comandos SQL, intenta subir un nuevo resultado desde el panel admin:

1. Ve a: http://127.0.0.1:5000/resultados
2. Click en "Nuevo Resultado"
3. Selecciona un paciente
4. **DEJA EL NÚMERO DE ORDEN VACÍO** (se generará automáticamente)
5. Selecciona fecha y archivo PDF
6. Click en "Guardar"

**Resultado esperado:**
```
✅ Resultado guardado exitosamente. Código de acceso: ABC123XY
```

---

## 🎯 Características del Nuevo Sistema

Una vez arreglada la base de datos:

### 1. Números de Orden Automáticos
- Formato: `YYYYMMDD-HHMMSS-XXX`
- Ejemplo: `20251107-153045-001`
- SIEMPRE únicos, nunca se repiten

### 2. Almacenamiento Robusto de PDFs
- Nombres únicos con timestamp
- Ejemplo: `20251107-153045-001_20251107_153046_123456_resultado.pdf`

### 3. Backups Automáticos
- Cada PDF se guarda en 2 lugares:
  - `/app/static/uploads/` (principal)
  - `/app/static/uploads/backups/` (respaldo)

### 4. Códigos de Acceso Únicos
- Siempre únicos y verificados
- 8 caracteres alfanuméricos
- Ejemplo: `N09KGKF9`

### 5. Manejo Inteligente de Errores
- Si falla la BD, se eliminan los archivos
- Nunca quedan archivos huérfanos
- Logs detallados en consola

---

## 📝 Logs de Confirmación

Cuando subes un resultado exitosamente, verás en la consola:

```
📋 Usando número de orden manual: 123
  (o)
🔢 Número de orden generado automáticamente: 20251107-153045-001

✓ PDF guardado: uploads/20251107-153045-001_20251107_153046_123456_resultado.pdf (245672 bytes)
✓ BACKUP creado: uploads/backups/20251107-153045-001_20251107_153046_123456_resultado.pdf

================================================================================
✅ RESULTADO GUARDADO EXITOSAMENTE
   ID: 5
   Número Orden: 20251107-153045-001
   Código Acceso: N09KGKF9
   Paciente: gonzalo higuain
   Archivo: 20251107-153045-001_20251107_153046_123456_resultado.pdf
   Backup: ✓ Creado
================================================================================
```

---

## ❓ Si Algo Sale Mal

Si después de ejecutar el SQL sigues teniendo problemas:

1. **Verifica que el SQL se ejecutó correctamente**
   ```sql
   SELECT constraint_name
   FROM information_schema.table_constraints
   WHERE table_name = 'resultados';
   ```

2. **Reinicia la aplicación Flask**
   - Detén el servidor (Ctrl+C)
   - Vuelve a ejecutar `python run.py` (o el comando que uses)

3. **Verifica los logs en la consola**
   - Busca mensajes de error
   - Comparte el output completo si necesitas ayuda

---

## 🚀 ¡Todo Listo!

Una vez ejecutados los comandos SQL, tu sistema estará:
- ✅ Sin restricciones de numero_orden
- ✅ Con generación automática de números únicos
- ✅ Con backups automáticos de PDFs
- ✅ Con manejo robusto de errores
- ✅ 100% funcional para múltiples resultados por paciente

**¡Nunca más perderás archivos PDF!** 🎉
