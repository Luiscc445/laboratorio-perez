# LABORATORIO PÉREZ - GUÍA DE PERSONALIZACIÓN

## ✅ Archivos Creados

1. `app/static/css/laboratorio_perez.css` - Estilos con colores del logo
2. `app/static/img/logo_perez.jpg` - Logo del laboratorio
3. `app/templates/auth/login_perez.html` - Login personalizado
4. `actualizacion_base_html.txt` - Código para base.html

## 🎨 Paleta de Colores

- **Naranja**: #F39C12, #E67E22 (botones principales)
- **Verde agua**: #1ABC9C, #16A085 (navbar, cards)
- **Blanco**: #FFFFFF (fondos)

## 📋 Pasos para Completar la Instalación

### 1. Actualizar base.html

Abre `app/templates/base.html` y agrega el siguiente código:

**En la sección `<head>` (después de los otros CSS):**
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/laboratorio_perez.css') }}">
<link rel="icon" type="image/jpeg" href="{{ url_for('static', filename='img/logo_perez.jpg') }}">
```

**En el navbar, reemplazar `<a class="navbar-brand">`:**
```html
<a class="navbar-brand" href="{{ url_for('index') }}">
    <img src="{{ url_for('static', filename='img/logo_perez.jpg') }}" alt="Laboratorio Pérez">
    Laboratorio Pérez
</a>
```

**Antes de `</body>`, agregar el footer** (copiar de actualizacion_base_html.txt)

### 2. Actualizar ruta de login (opcional)

Si quieres usar el login personalizado, en `app/routes.py` o donde tengas la ruta de login:

```python
@app.route('/auth/login')
def login():
    return render_template('auth/login_perez.html')
```

### 3. Reiniciar el servidor

```powershell
python run.py
```

### 4. Verificar

Abre en el navegador: http://localhost:5000

Deberías ver:
- ✅ Logo en el navbar
- ✅ Colores naranja y verde agua
- ✅ Footer con información de contacto
- ✅ Redes sociales (Facebook, WhatsApp)

## 📍 Información del Laboratorio

- **Nombre**: Laboratorio Pérez
- **Dirección**: La Paz entre Matos y Hoyos 1137, Potosí, Bolivia
- **Teléfono**: 67619188
- **WhatsApp**: +591 67619188
- **Email**: laboratorios.perez@gmail.com
- **Facebook**: https://www.facebook.com/LaboratoriosPerez

## 🐛 Solución de Problemas

### El logo no se ve
```powershell
# Verificar que existe:
Test-Path "app\static\img\logo_perez.jpg"

# Si no existe, copiarlo:
Copy-Item "$env:USERPROFILE\Downloads\logo_oficial.jpg" "app\static\img\logo_perez.jpg"
```

### Los estilos no se aplican
```powershell
# Verificar que existe el CSS:
Test-Path "app\static\css\laboratorio_perez.css"

# Limpiar caché del navegador: Ctrl+Shift+Delete
```

### Error 404 en archivos estáticos
Asegúrate que en `app/__init__.py` o `config.py` esté configurado:
```python
app.static_folder = 'static'
```

## ✨ Resultado Final

Tu sistema tendrá:
- 🏥 Identidad visual del Laboratorio Pérez
- 🎨 Colores profesionales del logo
- 📱 Enlaces a Facebook y WhatsApp
- 📍 Información de contacto visible
- ✅ Diseño moderno y responsive
