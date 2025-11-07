# 🚀 COMANDOS SIMPLES PARA ARREGLAR TODO

## ⚡ EJECUTA ESTOS COMANDOS (EN ORDEN):

### **1. Arreglar la Base de Datos**

```bash
python arreglar_base_datos.py
```

**Eso es todo!** El script hará:
- ✅ Eliminar restricción UNIQUE de numero_orden
- ✅ Agregar restricción UNIQUE a codigo_acceso
- ✅ Crear carpetas para PDFs y backups
- ✅ Verificar que todo quedó bien

---

### **2. Reiniciar Flask**

Detén Flask si está corriendo (Ctrl+C) y vuelve a ejecutar:

```bash
python run.py
```

O si usas otro comando, ejecuta el que normalmente uses.

---

### **3. Probar el Sistema**

1. Ve a: `http://127.0.0.1:5000/resultados`
2. Click en "Nuevo Resultado"
3. Selecciona un paciente
4. **Deja "Número de Orden" VACÍO**
5. Selecciona fecha y PDF
6. Click "Guardar"

**¡Listo!** Verás:
```
✅ Resultado guardado exitosamente. Código de acceso: ABC123XY
```

---

## 📋 RESUMEN

**Comandos completos:**

```bash
# Paso 1: Arreglar base de datos
python arreglar_base_datos.py

# Paso 2: Reiniciar Flask
python run.py
```

**Eso es TODO!** 🎉

---

## ✅ QUÉ ESPERAR

### **Cuando ejecutes `python arreglar_base_datos.py` verás:**

```
================================================================================
🔧 ARREGLANDO BASE DE DATOS - LABORATORIO PÉREZ
================================================================================

📡 Verificando conexión a la base de datos...
✅ Conectado a: postgres

🔍 Buscando restricción UNIQUE en numero_orden...
❌ Encontrada restricción problemática: resultados_numero_orden_key
   Esta restricción impide subir múltiples resultados.

🗑️  Eliminando restricción 'resultados_numero_orden_key'...
✅ Restricción 'resultados_numero_orden_key' eliminada exitosamente!

🔍 Verificando restricción UNIQUE en codigo_acceso...
➕ Agregando restricción UNIQUE a codigo_acceso...
✅ Restricción UNIQUE agregada a codigo_acceso!

📊 Estado final de la tabla 'resultados':
--------------------------------------------------------------------------------
   PRIMARY KEY     | id                   | resultados_pkey
   UNIQUE          | codigo_acceso        | resultados_codigo_acceso_unique
   FOREIGN KEY     | paciente_id          | resultados_paciente_id_fkey
--------------------------------------------------------------------------------

📁 Creando carpetas para PDFs...
✅ app/static/uploads/
✅ app/static/uploads/backups/
✅ app/static/uploads/pruebas/

================================================================================
🎉 BASE DE DATOS ARREGLADA EXITOSAMENTE
================================================================================

✅ CAMBIOS REALIZADOS:
   • Restricción UNIQUE eliminada de 'numero_orden'
   • Restricción UNIQUE agregada a 'codigo_acceso'
   • Carpetas de uploads creadas correctamente

🚀 AHORA PUEDES:
   • Subir múltiples resultados al mismo paciente
   • El sistema generará números de orden automáticos
   • Cada PDF se guarda con backup automático
   • Nunca se perderán archivos

📝 PRÓXIMO PASO:
   1. Reinicia Flask (Ctrl+C y vuelve a ejecutar)
   2. Ve a: http://127.0.0.1:5000/resultados
   3. Sube un nuevo resultado (deja número de orden vacío)
   4. ¡Disfruta del sistema robusto!

================================================================================
```

---

## ❓ SI HAY ALGÚN ERROR

### **Error: "ModuleNotFoundError"**
Activa tu entorno virtual primero:

**Windows:**
```bash
venv\Scripts\activate
python arreglar_base_datos.py
```

**Linux/Mac:**
```bash
source venv/bin/activate
python arreglar_base_datos.py
```

### **Error: "No module named 'app'"**
Asegúrate de estar en la carpeta del proyecto:
```bash
cd C:\misistempp
python arreglar_base_datos.py
```

### **Error de conexión a base de datos**
Verifica tu archivo `.env`:
```
DATABASE_URL=postgresql://...
SUPABASE_URL=...
SUPABASE_KEY=...
```

---

## 🎯 DESPUÉS DE ARREGLAR

**Puedes subir INFINITOS resultados al mismo paciente:**

- Paciente: "gonzalo higuain"
  - ✅ Resultado 1: Número orden `20251107-153045-001`
  - ✅ Resultado 2: Número orden `20251107-154012-001`
  - ✅ Resultado 3: Número orden `20251107-155233-001`
  - ✅ Resultado 4: Número orden `20251107-160545-001`
  - ... (sin límite!)

**Cada uno con su PDF guardado y respaldado!** 💪

---

## 📞 NECESITAS AYUDA?

El script es muy verboso y te dirá exactamente qué está pasando.

Si algo falla, copia TODO el output del comando y compártelo.

---

**¡EJECUTA Y DISFRUTA!** 🚀
