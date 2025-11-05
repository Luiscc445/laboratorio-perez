# 🖼️ Instrucciones para Agregar Imágenes Profesionales a Todas las Pruebas

Este documento explica cómo usar el script `poblar_pruebas_con_imagenes.py` para asignar **imágenes profesionales únicas** a cada una de las 176+ pruebas de laboratorio.

## 🎯 ¿Qué hace este script?

- **Analiza el nombre de CADA prueba individual**
- **Genera keywords inteligentes** basados en el contenido
- **Busca imágenes profesionales** específicas para cada prueba
- **Descarga y asigna una imagen fija única** a cada prueba
- Cada prueba tiene su propia imagen (no se comparten entre pruebas)

## 📸 Servicios de Imágenes Disponibles

### Opción 1: **Pexels API** (Recomendado) ⭐

**Ventajas:**
- ✅ Completamente GRATUITO
- ✅ Imágenes de alta calidad profesional
- ✅ 200 búsquedas por hora (suficiente para todas las pruebas)
- ✅ Sin marca de agua
- ✅ Búsqueda inteligente por keywords

**Cómo obtener tu API Key:**

1. Ve a: **https://www.pexels.com/api/**
2. Clic en **"Get Started"**
3. Regístrate gratis (email + contraseña)
4. Ve a tu dashboard
5. Copia tu **API Key** (algo como: `ABC123XYZ...`)

### Opción 2: **Unsplash Source** (Sin API Key)

**Ventajas:**
- ✅ No requiere registro ni API key
- ✅ Imágenes de alta calidad
- ⚠️ Menos control sobre las búsquedas
- ⚠️ Búsquedas más genéricas

## 🚀 Cómo Usar el Script

### Con Pexels (Recomendado):

1. **Obtén tu API Key de Pexels** (ver arriba)

2. **Edita el archivo:**
   ```bash
   notepad poblar_pruebas_con_imagenes.py
   ```

3. **Busca esta línea (línea 17):**
   ```python
   PEXELS_API_KEY = "TU_API_KEY_AQUI"
   ```

4. **Reemplaza con tu API Key:**
   ```python
   PEXELS_API_KEY = "ABC123XYZ456..."  # Tu API key real
   ```

5. **Guarda el archivo**

6. **Ejecuta el script:**
   ```powershell
   # Activar entorno virtual
   .\venv\Scripts\activate

   # Ejecutar script
   python poblar_pruebas_con_imagenes.py
   ```

### Sin API Key (Unsplash):

1. **Edita el archivo:**
   ```bash
   notepad poblar_pruebas_con_imagenes.py
   ```

2. **Busca esta línea (línea 20):**
   ```python
   USE_PEXELS = True
   ```

3. **Cámbiala a:**
   ```python
   USE_PEXELS = False
   ```

4. **Ejecuta el script:**
   ```powershell
   .\venv\Scripts\activate
   python poblar_pruebas_con_imagenes.py
   ```

## 📊 Proceso Completo Paso a Paso

```powershell
# 1. Descargar cambios
git pull origin claude/fix-hamburger-mobile-view-011CUjDSifEHg1fGrNcWbiT7 --no-edit

# 2. Activar entorno virtual
.\venv\Scripts\activate

# 3. ELIMINAR todas las pruebas viejas (opcional, empezar limpio)
python eliminar_todas_pruebas.py
# Confirmar: SI + ELIMINAR TODO

# 4. POBLAR con imágenes individuales
python poblar_pruebas_con_imagenes.py
# Espera ~5-10 minutos (descarga 176+ imágenes)

# 5. Ejecutar aplicación
python run.py
```

## 🎨 Sistema de Keywords Inteligente

El script analiza cada prueba y genera keywords específicos:

### Ejemplos:

| Prueba | Keywords Generados | Tipo de Imagen |
|--------|-------------------|----------------|
| HEMOGRAMA | "blood test cells laboratory medical" | Células sanguíneas |
| GLUCOSA BASAL | "glucose blood sugar laboratory medical" | Glucómetro/azúcar |
| HEPATITIS B | "hepatitis liver laboratory medical" | Hígado/hepatitis |
| CULTIVO Y ANTIBIOGRAMA | "bacterial culture laboratory medical" | Placa de petri |
| VITAMINA B12 | "vitamin supplement laboratory medical" | Vitaminas |
| VIH | "hiv test laboratory medical" | Test VIH |

Cada prueba obtiene una imagen **única y relevante** basada en su contenido específico.

## 📁 ¿Dónde se Guardan las Imágenes?

```
app/static/uploads/pruebas/
├── prueba_a1b2c3d4e5f6.jpg  (HEMOGRAMA)
├── prueba_f6e5d4c3b2a1.jpg  (GLUCOSA)
├── prueba_123456789abc.jpg  (HEPATITIS B)
└── ... (176+ imágenes)
```

- Nombres únicos con hash MD5 (evita conflictos)
- Formato: `prueba_[hash].jpg`
- Resolución: 800x600 o 350px de ancho (optimizado web)

## ⏱️ Tiempo Estimado

- **Con Pexels:** ~5-8 minutos (incluye rate limiting de 1 segundo entre requests)
- **Con Unsplash:** ~3-5 minutos (sin rate limiting estricto)

## ⚠️ Notas Importantes

1. **Rate Limiting:** El script incluye pausas automáticas para no exceder límites
2. **Imágenes Fijas:** Una vez asignada, la imagen NO cambia (es fija para esa prueba)
3. **Internet Requerido:** Necesitas conexión para descargar las imágenes
4. **Primera Ejecución:** Solo descarga imágenes nuevas, no duplica si ya existen

## 🆘 Solución de Problemas

### Error: "No se encontró imagen"
- **Causa:** Keywords muy específicos sin resultados
- **Solución:** El script usa placeholder genérico de la categoría

### Error: "API Key inválida"
- **Causa:** API Key incorrecta o mal copiada
- **Solución:** Verifica que copiaste toda la key sin espacios

### Error: "Rate limit exceeded"
- **Causa:** Demasiadas búsquedas rápidas
- **Solución:** Espera 1 hora y vuelve a ejecutar

### Imágenes no aparecen en la web
- **Causa:** Ruta incorrecta
- **Solución:** Verifica que `app/static/uploads/pruebas/` existe

## ✅ Resultado Final

Después de ejecutar el script:

- ✅ 176+ pruebas con imágenes profesionales únicas
- ✅ Cada prueba tiene una imagen relevante a su contenido
- ✅ Imágenes optimizadas para web
- ✅ Catálogo visualmente profesional y atractivo

## 🎉 ¡Listo!

Tu catálogo ahora tendrá imágenes profesionales individuales para cada prueba. Los usuarios podrán ver visualmente qué tipo de prueba es antes de leer la descripción.
