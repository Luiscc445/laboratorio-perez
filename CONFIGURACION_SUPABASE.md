# 🔄 CONFIGURACIÓN COMPLETA DE SUPABASE - LABORATORIO PÉREZ

## 📋 NUEVA CUENTA DE SUPABASE

Has migrado a una nueva cuenta de Supabase. Esta guía te ayudará a configurar todo desde cero.

---

## 🎯 PASO 1: OBTENER LA URL DE CONEXIÓN POSTGRESQL

### 1.1 Acceder a Supabase Dashboard

1. Ve a [https://supabase.com](https://supabase.com)
2. Inicia sesión en tu cuenta
3. Selecciona tu proyecto: `vzkfbrwjtmivnvjyjeqi`

### 1.2 Obtener Database Password

1. En el dashboard, ve a **Settings** (⚙️ en la barra lateral)
2. Click en **Database**
3. Busca la sección **"Database Settings"**
4. Aquí verás tu **Database Password** (si la olvidaste, puedes resetearla)
5. **COPIA esta contraseña** - la necesitarás para el siguiente paso

### 1.3 Obtener Connection String

1. En la misma página (Settings > Database)
2. Busca la sección **"Connection string"**
3. Selecciona la pestaña **"URI"**
4. Asegúrate de seleccionar **"Session mode"** (NO Pooler mode)
5. Verás algo como:

```
postgresql://postgres.vzkfbrwjtmivnvjyjeqi:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

6. **Reemplaza `[YOUR-PASSWORD]`** con la contraseña que copiaste en el paso 1.2
7. **COPIA esta URL completa** - la usarás en el archivo .env

---

## 💻 PASO 2: CONFIGURAR TU PROYECTO LOCAL

### 2.1 Obtener los cambios del repositorio

Abre PowerShell en `C:\misistempp`:

```powershell
cd C:\misistempp
git pull origin claude/fix-hamburger-mobile-view-011CUjDSifEHg1fGrNcWbiT7
```

### 2.2 Crear el archivo .env

1. Copia el archivo de ejemplo:

```powershell
copy .env.example .env
```

2. Abre `.env` con tu editor de texto (Notepad, VSCode, etc.)

3. Reemplaza `[TU_PASSWORD_POSTGRESQL]` con la contraseña real que obtuviste

**ANTES:**
```env
DATABASE_URL=postgresql://postgres.vzkfbrwjtmivnvjyjeqi:[TU_PASSWORD_POSTGRESQL]@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

**DESPUÉS (ejemplo):**
```env
DATABASE_URL=postgresql://postgres.vzkfbrwjtmivnvjyjeqi:tu_contraseña_real_aqui@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

4. Opcionalmente, cambia el `SECRET_KEY` por una cadena aleatoria:

```env
SECRET_KEY=mi_clave_super_secreta_12345_cambiame
```

5. **GUARDA el archivo** `.env`

### 2.3 Verificar las credenciales en .env

Tu archivo `.env` debe tener estas variables configuradas:

```env
# Flask
SECRET_KEY=tu_clave_secreta_aqui

# Supabase API
SUPABASE_URL=https://vzkfbrwjtmivnvjyjeqi.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ6a2ZicndqdG1pdm52anlqZXFpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIxOTAxNTAsImV4cCI6MjA3Nzc2NjE1MH0.S3ccnlklLDI0c-5klGLumz3f-N1P5Y-W_o66MLBzNo8
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ6a2ZicndqdG1pdm52anlqZXFpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MjE5MDE1MCwiZXhwIjoyMDc3NzY2MTUwfQ.JWd-AYFggx36nO5GZNuOGac8I6-xWYzOlZa2wadAPvg

# PostgreSQL Connection
DATABASE_URL=postgresql://postgres.vzkfbrwjtmivnvjyjeqi:TU_PASSWORD_AQUI@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

---

## 🗄️ PASO 3: CREAR LAS TABLAS EN SUPABASE

### 3.1 Abrir SQL Editor en Supabase

1. Ve a tu proyecto en Supabase Dashboard
2. Click en **SQL Editor** (📊 en la barra lateral)
3. Click en **"New Query"**

### 3.2 Ejecutar el script SQL

1. Abre el archivo `supabase_setup.sql` en tu computadora
2. **COPIA TODO EL CONTENIDO** del archivo
3. **PÉGALO** en el SQL Editor de Supabase
4. Click en **"Run"** o presiona `Ctrl+Enter`

### 3.3 Verificar que se crearon las tablas

Deberías ver un mensaje de éxito. Luego ejecuta esta query para verificar:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

**Resultado esperado:**
- `pacientes`
- `pruebas`
- `resultados`
- `usuarios`

✅ ¡Perfecto! Las tablas se crearon correctamente.

---

## 👤 PASO 4: CREAR EL USUARIO ADMINISTRADOR

### 4.1 Activar entorno virtual

En PowerShell:

```powershell
cd C:\misistempp
.\venv\Scripts\Activate.ps1
```

### 4.2 Ejecutar el script de creación de admin

```powershell
python create_admin.py
```

### 4.3 Salida esperada

```
======================================================================
🔒 SISTEMA DE SEGURIDAD - LABORATORIO PÉREZ
======================================================================

🔍 PASO 1: Verificando usuarios existentes en Supabase...

✅ No hay usuarios antiguos. Base de datos limpia.

🔧 PASO 2: Creando nuevo usuario administrador...

======================================================================
✅ USUARIO ADMINISTRADOR CREADO EXITOSAMENTE EN SUPABASE
======================================================================

📋 DATOS DEL ADMINISTRADOR:
   • ID en Supabase: 1
   • Usuario: DoctorMauricoPerezPTS574
   • Contraseña: Cachuchin574
   • Rol: Administrador (is_admin=True)
   • Hash en BD: pbkdf2:sha256:600000$xxxxx...
   • Fecha creación: 2025-11-03 XX:XX:XX

======================================================================
🔒 INFORMACIÓN DE SEGURIDAD:
======================================================================
   ✓ Contraseña hasheada con Werkzeug (pbkdf2:sha256)
   ✓ Solo este usuario puede acceder al sistema administrativo
   ✓ Todas las rutas admin protegidas con @admin_required
   ✓ Hash almacenado de forma segura en Supabase

======================================================================
🌐 ACCESO AL SISTEMA:
======================================================================
   URL: http://localhost:5000/auth/login
   Usuario: DoctorMauricoPerezPTS574
   Contraseña: Cachuchin574

======================================================================
⚠️  GUARDA ESTAS CREDENCIALES EN UN LUGAR SEGURO
======================================================================
```

### 4.4 Verificar en Supabase

Vuelve a Supabase SQL Editor y ejecuta:

```sql
SELECT id, username, is_admin,
       LEFT(password_hash, 30) as hash_preview,
       fecha_creacion
FROM usuarios;
```

**Resultado esperado:**

| id | username | is_admin | hash_preview | fecha_creacion |
|----|----------|----------|--------------|----------------|
| 1 | DoctorMauricoPerezPTS574 | true | pbkdf2:sha256:600000$xxxxx | 2025-11-03... |

---

## 🚀 PASO 5: INICIAR EL SISTEMA

### 5.1 Iniciar el servidor Flask

```powershell
python run.py
```

Deberías ver:

```
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

### 5.2 Acceder al sistema

1. Abre tu navegador
2. Ve a: **http://localhost:5000/auth/login**
3. Ingresa las credenciales:
   - **Usuario:** `DoctorMauricoPerezPTS574`
   - **Contraseña:** `Cachuchin574`
4. ✅ Deberías ser redirigido al Dashboard Administrativo

---

## 📁 ARCHIVOS NUEVOS CREADOS

```
laboratorio-perez/
├── .env.example              ✅ Template de configuración
├── supabase_setup.sql        ✅ Script SQL completo
├── CONFIGURACION_SUPABASE.md ✅ Esta guía
├── create_admin.py           ✅ Script para crear admin (ya existía)
└── .env                      ⚠️  (debes crearlo tú)
```

---

## 🔍 VERIFICACIÓN FINAL

### ✅ Checklist de Verificación

- [ ] 1. Obtuve la contraseña de PostgreSQL de Supabase
- [ ] 2. Copié .env.example a .env
- [ ] 3. Configuré DATABASE_URL con la contraseña real en .env
- [ ] 4. Ejecuté el SQL en Supabase (supabase_setup.sql)
- [ ] 5. Verifiqué que se crearon 4 tablas
- [ ] 6. Ejecuté python create_admin.py
- [ ] 7. Vi el mensaje de éxito
- [ ] 8. Verifiqué en Supabase que existe el usuario admin
- [ ] 9. Inicié el servidor con python run.py
- [ ] 10. Pude hacer login correctamente

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Problema: "ModuleNotFoundError: No module named 'dotenv'"

**Solución:**
```powershell
pip install python-dotenv
```

### Problema: "ERROR: Connection to database failed"

**Solución:**
1. Verifica que DATABASE_URL en .env tiene la contraseña correcta
2. Verifica que copiaste la URL completa sin espacios
3. Intenta resetear la contraseña en Supabase > Settings > Database

### Problema: "Table 'usuarios' doesn't exist"

**Solución:**
1. Ejecuta nuevamente el SQL completo en Supabase
2. Verifica que estás conectado a la base de datos correcta

### Problema: "Usuario o contraseña incorrectos"

**Solución:**
1. Ejecuta nuevamente: `python create_admin.py`
2. Verifica en Supabase que el usuario existe:
   ```sql
   SELECT * FROM usuarios;
   ```

---

## 📊 ESTRUCTURA DE LA BASE DE DATOS

### Tablas creadas:

1. **usuarios** - Usuarios del sistema administrativo
   - username (único)
   - password_hash (hasheado)
   - is_admin (rol)

2. **pacientes** - Información de pacientes
   - nombre, ci (único), telefono, email
   - fecha_registro

3. **resultados** - Resultados de laboratorio
   - numero_orden (único)
   - paciente_id (FK a pacientes)
   - codigo_acceso (para consulta pública)
   - archivo_pdf

4. **pruebas** - Catálogo de pruebas
   - nombre, categoria, descripcion
   - precio, imagen

---

## 🔐 CREDENCIALES FINALES

### Usuario Administrador:

```
Usuario:    DoctorMauricoPerezPTS574
Contraseña: Cachuchin574
Rol:        Administrador (is_admin=True)
URL:        http://localhost:5000/auth/login
```

### Supabase API:

```
URL:        https://vzkfbrwjtmivnvjyjeqi.supabase.co
ANON Key:   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...S3ccnlklLDI0c-5klGLumz3f-N1P5Y-W_o66MLBzNo8
SERVICE:    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...JWd-AYFggx36nO5GZNuOGac8I6-xWYzOlZa2wadAPvg
```

---

## ⚠️ SEGURIDAD

1. **NUNCA compartas tu archivo `.env`**
2. **NUNCA subas `.env` a Git** (ya está en .gitignore)
3. **Guarda las credenciales en un lugar seguro** (gestor de contraseñas)
4. **La contraseña está hasheada** en Supabase y no se puede recuperar
5. Si olvidas la contraseña, ejecuta nuevamente `python create_admin.py`

---

**Última actualización:** 2025-11-03
**Versión:** 2.0
**Nueva base de datos:** Supabase (vzkfbrwjtmivnvjyjeqi)
