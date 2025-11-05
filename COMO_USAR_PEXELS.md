# 📸 Cómo Usar Pexels para Descargar Imágenes

## ✅ Pexels es 100% GRATIS

## 🚀 Pasos Rápidos (5 minutos):

### 1. Obtener API Key de Pexels (2 minutos)

1. **Ve a:** https://www.pexels.com/api/
2. **Clic en** "Get Started" (botón verde)
3. **Regístrate:**
   - Puedes usar Google/Facebook o email
   - Completa nombre y email
   - Acepta términos
4. **Verificar email** (si usas email directo)
5. **Ir al Dashboard:**
   - Automáticamente te redirige a tu dashboard
   - O ve a: https://www.pexels.com/api/documentation/
6. **Copiar tu API Key:**
   - Verás tu API Key en la parte superior
   - Se ve algo así: `ABC123def456GHI789jkl012MNO345pqr678`
   - ¡Cópiala completa!

### 2. Configurar el Script

1. **Abre el archivo:**
   ```powershell
   notepad setup_con_pexels.py
   ```

2. **Busca la línea 20** que dice:
   ```python
   PEXELS_API_KEY = "PONER_TU_API_KEY_AQUI"
   ```

3. **Reemplaza** con tu API Key:
   ```python
   PEXELS_API_KEY = "ABC123def456GHI789jkl012MNO345pqr678"
   ```
   (usa tu key real, no esta de ejemplo)

4. **Guarda** el archivo (Ctrl+S)

### 3. Ejecutar el Script

```powershell
# Ya debes tener descargado todo:
git pull origin claude/fix-hamburger-mobile-view-011CUjDSifEHg1fGrNcWbiT7 --no-edit

# Activar entorno virtual
.\venv\Scripts\activate

# Ejecutar script con Pexels
python setup_con_pexels.py

# Confirmar con: SI

# Esperar ~8-10 minutos
# Verás el progreso de cada imagen descargada

# Cuando termine, ejecutar app
python run.py
```

## 📊 Límites de Pexels (GRATIS):

- ✅ 200 búsquedas por hora
- ✅ Perfecto para 176 pruebas (solo usará 176 búsquedas)
- ✅ Imágenes de alta calidad
- ✅ Sin marca de agua
- ✅ Gratis para siempre

## 🎯 Resultado:

Cada una de las 176+ pruebas tendrá su propia imagen profesional de Pexels:

- 🩸 HEMOGRAMA → Imagen profesional de células sanguíneas
- 🍬 GLUCOSA → Imagen profesional de glucómetro
- 🦠 CULTIVO → Imagen profesional de placa petri
- 💊 VITAMINAS → Imagen profesional de suplementos
- ... ¡y 172+ más con imágenes únicas profesionales!

## ⚠️ Solución de Problemas

### "ModuleNotFoundError: No module named 'requests'"
```powershell
pip install requests
```

### "API Key inválida"
- Verifica que copiaste toda la key sin espacios
- No debe tener comillas extra
- Debe estar entre comillas simples o dobles

### "Rate limit exceeded"
- Espera 1 hora
- O ejecuta el script más tarde

## 💡 Alternativa Sin API Key:

Si no quieres registrarte en Pexels, usa:
```powershell
python setup_rapido_sin_imagenes.py
```

Esto crea todas las pruebas SIN imágenes en 5 segundos.
Las imágenes mostrarán un placeholder visual bonito.

## ✅ ¡Eso es todo!

Una vez que tengas tu API Key y la configures, el script hace TODO automáticamente.
