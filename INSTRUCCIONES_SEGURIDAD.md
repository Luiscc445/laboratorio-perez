# 🔐 INSTRUCCIONES DE SEGURIDAD - LABORATORIO PÉREZ

Sistema de autenticación segura con Supabase

---

## 📋 PARTE 1: CONFIGURACIÓN EN SUPABASE

### Paso 1: Abrir Supabase SQL Editor

1. Ir a tu proyecto en [Supabase](https://supabase.com)
2. Click en "SQL Editor" en el menú lateral
3. Click en "New Query"

### Paso 2: Ejecutar el siguiente SQL

```sql
-- ============================================================
-- LIMPIEZA Y CREACIÓN DE USUARIO ADMINISTRADOR
-- ============================================================

-- 1. Eliminar todos los usuarios antiguos
DELETE FROM usuarios;

-- 2. Resetear el ID auto-incremental (opcional)
ALTER SEQUENCE usuarios_id_seq RESTART WITH 1;

-- 3. Verificar estructura de la tabla
-- Si la tabla NO existe, créala primero:
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

-- 4. Verificar que la tabla esté vacía
SELECT * FROM usuarios;
-- Resultado esperado: 0 rows (tabla vacía)
```

### Paso 3: Verificar que se ejecutó correctamente

✅ Deberías ver: "Success. No rows returned"

---

## 💻 PARTE 2: CONFIGURACIÓN EN TU COMPUTADORA (WINDOWS)

### Paso 1: Obtener los cambios del repositorio

Abre PowerShell en la carpeta del proyecto:

```powershell
cd C:\misistempp

# Obtener los últimos cambios
git pull origin claude/fix-hamburger-mobile-view-011CUjDSifEHg1fGrNcWbiT7
```

### Paso 2: Activar el entorno virtual

```powershell
.\venv\Scripts\Activate.ps1
```

### Paso 3: Crear el usuario administrador

```powershell
python create_admin.py
```

**Salida esperada:**

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
   • Hash en BD: pbkdf2:sha256:600000$xxxxxxxxxxxxx...
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

### Paso 4: Verificar en Supabase

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

## 🚀 PARTE 3: INICIAR EL SISTEMA

### Paso 1: Iniciar el servidor Flask

```powershell
python run.py
```

### Paso 2: Acceder al sistema

1. Abre tu navegador
2. Ve a: `http://localhost:5000/auth/login`
3. Ingresa las credenciales:
   - **Usuario:** `DoctorMauricoPerezPTS574`
   - **Contraseña:** `Cachuchin574`

---

## 🛡️ CARACTERÍSTICAS DE SEGURIDAD

### ✅ Implementaciones de Seguridad

1. **Contraseña Hasheada**
   - Algoritmo: `pbkdf2:sha256` con 600,000 iteraciones
   - La contraseña NUNCA se guarda en texto plano
   - Hash diferente cada vez (incluye salt aleatorio)

2. **Decorador @admin_required**
   - Protege todas las rutas administrativas
   - Valida autenticación + rol de administrador
   - Redirige automáticamente si no hay permisos

3. **Rutas Protegidas**
   - `/dashboard` - Solo admin
   - `/pacientes/*` - Solo admin
   - `/resultados/*` - Solo admin
   - `/pruebas/*` - Solo admin
   - Rutas públicas sin restricción

4. **Sesiones Seguras**
   - Flask-Login maneja las sesiones
   - Cookie segura con secret_key
   - Auto-logout al cerrar navegador (opcional)

---

## 📁 ARCHIVOS DEL SISTEMA DE SEGURIDAD

```
laboratorio-perez/
├── app/
│   ├── utils.py              # Decorador @admin_required
│   ├── models.py             # Modelo Usuario con hash
│   ├── auth.py               # Rutas de login/logout
│   └── routes.py             # Rutas protegidas
├── create_admin.py           # Script de creación de admin
└── INSTRUCCIONES_SEGURIDAD.md  # Este archivo
```

---

## 🔍 VERIFICACIÓN Y PRUEBAS

### Verificar usuario en Supabase

```sql
-- Ver todos los datos del usuario
SELECT * FROM usuarios WHERE username = 'DoctorMauricoPerezPTS574';

-- Contar usuarios (debe ser 1)
SELECT COUNT(*) FROM usuarios;

-- Ver solo administradores
SELECT username, is_admin FROM usuarios WHERE is_admin = TRUE;
```

### Probar el sistema

1. **Login exitoso:**
   - Usuario: `DoctorMauricoPerezPTS574`
   - Contraseña: `Cachuchin574`
   - ✅ Debe redirigir al dashboard

2. **Login fallido:**
   - Usuario incorrecto o contraseña incorrecta
   - ❌ Debe mostrar: "Usuario o contraseña incorrectos"

3. **Acceso directo sin login:**
   - Ir a: `http://localhost:5000/dashboard`
   - ❌ Debe redirigir a login

---

## ⚠️ NOTAS IMPORTANTES

1. **NO compartas las credenciales** con nadie
2. **Guarda las credenciales** en un gestor de contraseñas
3. **La contraseña en Supabase** está hasheada y no se puede recuperar
4. Si olvidas la contraseña, ejecuta nuevamente `python create_admin.py`
5. **Backup de Supabase:** Supabase hace backups automáticos

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Problema: "Usuario no encontrado"
**Solución:** Verifica que ejecutaste `python create_admin.py` correctamente

### Problema: "Contraseña incorrecta"
**Solución:**
1. Ejecuta nuevamente `python create_admin.py`
2. Verifica que no haya espacios al copiar la contraseña

### Problema: "No tienes permisos"
**Solución:**
1. Verifica en Supabase: `SELECT is_admin FROM usuarios;`
2. Debe ser `TRUE`

### Problema: El script create_admin.py da error
**Solución:**
1. Verifica conexión a Supabase
2. Revisa las variables de entorno en `.env`
3. Verifica que la tabla `usuarios` existe

---

## 📞 CONTACTO

Para soporte técnico sobre este sistema de seguridad, contacta al desarrollador.

---

**Última actualización:** 2025-11-03
**Versión del sistema:** 1.0
**Base de datos:** Supabase PostgreSQL
