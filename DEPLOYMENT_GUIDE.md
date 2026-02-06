# 🚀 DEPLOYMENT GUIDE - Weather Calendar Plugin a Raspberry Pi

**Fecha**: 6 de Febrero, 2026  
**Status**: ✅ Listo para producción

---

## 📋 Pre-requisitos

Antes de empezar, asegúrate de tener:

- ✅ Raspberry Pi con InkyPi instalado (o instalación limpia de Raspbian)
- ✅ E-ink display conectada (Pimoroni Inky o Waveshare)
- ✅ Conexión SSH disponible
- ✅ Git instalado en la Pi
- ✅ Acceso de superusuario (sudo)

---

## 🔧 Opción 1: Update Rápido (Si ya tienes InkyPi instalado)

### Paso 1: Conectarse por SSH

```bash
ssh pi@raspberrypi.local
# O si tienes la IP directa:
# ssh pi@192.168.1.100
```

### Paso 2: Entrar al directorio de InkyPi

```bash
cd /opt/inkypi
```

### Paso 3: Actualizar el código

```bash
# Stash any local changes
sudo git stash

# Pull latest changes
sudo git pull origin main

# Verificar que el plugin está ahí
ls -la src/plugins/weather_calendar/
```

**Output esperado:**
```
total 40
-rw-r--r-- 1 root root  224 Feb  6 18:00 weather_calendar.py
-rw-r--r-- 1 root root  8.2K Feb  6 18:00 icon.png
-rw-r--r-- 1 root root   2.1K Feb  6 18:00 plugin-info.json
-rw-r--r-- 1 root root   12K Feb  6 18:00 settings.html
drwxr-xr-x 2 root root  4.0K Feb  6 18:00 render/
```

### Paso 4: Instalar dependencias

```bash
# Activar venv
source venv/bin/activate

# Instalar requirements
pip install -r install/requirements-dev.txt

# O instalar solo lo nuevo:
pip install icalendar recurring-ical-events
```

### Paso 5: Reiniciar servicio

```bash
# Detener servicio
sudo systemctl stop inkypi

# Iniciar servicio
sudo systemctl start inkypi

# Verificar que está corriendo
sudo systemctl status inkypi

# Ver logs
sudo journalctl -u inkypi -f
```

---

## 🔧 Opción 2: Instalación Limpia (Sin InkyPi previo)

### Paso 1: Preparar Raspberry Pi

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    chromium-browser \
    libopenjp2-7 \
    libtiff5
```

### Paso 2: Clonar repositorio

```bash
cd /opt
sudo git clone https://github.com/fatihak/inkypi.git
cd inkypi
```

### Paso 3: Crear venv e instalar dependencias

```bash
# Crear virtual environment
sudo python3 -m venv venv

# Activar venv
source venv/bin/activate

# Instalar requirements
sudo pip install -r install/requirements-dev.txt

# Deactivar venv
deactivate
```

### Paso 4: Configurar display

Editar `/opt/inkypi/src/config/device.json`:

```bash
sudo nano src/config/device.json
```

Contenido para **Pimoroni Inky 7.3"** (recomendado):

```json
{
    "name": "InkyPi",
    "display_type": "inky",
    "resolution": [800, 480],
    "orientation": "horizontal",
    "timezone": "Europe/Madrid",
    "time_format": "24h",
    "playlist_config": {
        "enabled": true,
        "rotation_interval": 300
    }
}
```

**Nota**: Reemplaza `Europe/Madrid` con tu zona horaria.

### Paso 5: Instalar servicio systemd

```bash
# Copiar archivo del servicio
sudo cp install/inkypi.service /etc/systemd/system/

# Copiar script CLI
sudo cp install/inkypi /usr/local/bin/
sudo chmod +x /usr/local/bin/inkypi

# Recargar systemd
sudo systemctl daemon-reload

# Habilitar servicio al inicio
sudo systemctl enable inkypi

# Iniciar servicio
sudo systemctl start inkypi

# Verificar estado
sudo systemctl status inkypi
```

---

## ⚙️ Configurar Weather Calendar Plugin

### Opción A: Por Web UI (Recomendado)

```bash
# Abrir navegador en tu computadora
open http://raspberrypi.local:5000

# O usa la IP:
# open http://192.168.1.100:5000
```

**En la interfaz web:**

1. Haz clic en **Plugins**
2. Busca **Weather + Calendar**
3. Haz clic en **Settings**
4. Completa los campos:

| Campo | Ejemplo | Descripción |
|-------|---------|-------------|
| **Latitude** | 40.7128 | Tu latitud (NYC: 40.7128) |
| **Longitude** | -74.0060 | Tu longitud (NYC: -74.0060) |
| **Units** | metric | metric (°C) o imperial (°F) |
| **Calendar URLs** | (opcional) | URLs de calendarios iCloud |

5. Haz clic en **Display** para ver la previsualización
6. Haz clic en **Save** para guardar

### Opción B: Por SSH (Configuración Manual)

```bash
# SSH a la Pi
ssh pi@raspberrypi.local

# Editar archivo de configuración del plugin
sudo nano /opt/inkypi/src/plugins/weather_calendar/config.json
```

Crear archivo con contenido:

```json
{
    "latitude": "40.7128",
    "longitude": "-74.0060",
    "units": "metric",
    "calendarURLs[]": [
        "https://p123-caldav.icloud.com/published/..."
    ]
}
```

---

## 🔍 Verificar que Funciona

### Test 1: Ver logs en tiempo real

```bash
sudo journalctl -u inkypi -f
```

Deberías ver algo como:
```
Feb 06 18:34:22 raspberrypi inkypi[1234]: INFO - Initializing Weather Calendar plugin
Feb 06 18:34:23 raspberrypi inkypi[1234]: INFO - Fetching weather from Open-Meteo API
Feb 06 18:34:24 raspberrypi inkypi[1234]: INFO - Rendering image: 800x480
Feb 06 18:34:25 raspberrypi inkypi[1234]: INFO - Image updated successfully
```

### Test 2: Ver la imagen generada

```bash
# SSH a Pi
ssh pi@raspberrypi.local

# Ver última imagen
file /opt/inkypi/src/static/images/current_image.png

# Descargar a tu Mac para inspeccionar
scp pi@raspberrypi.local:/opt/inkypi/src/static/images/current_image.png ~/Downloads/
```

### Test 3: Test manual del plugin

```bash
# SSH a Pi
ssh pi@raspberrypi.local

# Entrar a directorio
cd /opt/inkypi

# Activar venv
source venv/bin/activate

# Ejecutar test
python3 << 'EOF'
import sys
sys.path.insert(0, 'src')

from plugins.weather_calendar.weather_calendar import WeatherCalendar
from config import Config

# Cargar config
config = Config()

# Crear plugin
plugin_config = {
    'id': 'weather_calendar',
    'class': 'WeatherCalendar'
}

plugin = WeatherCalendar(plugin_config)

# Configuración de prueba
settings = {
    'latitude': '40.7128',
    'longitude': '-74.0060',
    'units': 'metric',
    'calendarURLs[]': []
}

# Generar imagen
image = plugin.generate_image(settings, config)

if image:
    print("✅ Plugin works! Image size:", image.size)
else:
    print("❌ Error generating image")
EOF
```

---

## 📱 Opcional: Obtener URLs de Calendario iCloud

Si quieres mostrar eventos de hoy:

### Paso 1: Acceder a iCloud.com

1. Abre https://www.icloud.com
2. Inicia sesión con tu Apple ID
3. Abre **Calendar**

### Paso 2: Encontrar URL del calendario

1. Haz clic derecho en el calendario que quieras compartir
2. Selecciona **Share Calendar** (Compartir Calendario)
3. Marca "Public Calendar" (Calendario Público)
4. Copia el URL público

**Debería verse como:**
```
https://p123-caldav.icloud.com/published/xyz123/
```

### Paso 3: Agregar a configuración

En la web UI de InkyPi:
1. Plugins → Weather + Calendar → Settings
2. Pega la URL en el campo "Calendar URLs"
3. Haz clic en "Add Calendar" para agregar más
4. Guarda

---

## 🔧 Troubleshooting

### Problema: "Plugin not showing"

```bash
# Verificar que plugin existe
ls -la src/plugins/weather_calendar/

# Revisar logs
sudo journalctl -u inkypi -n 50 | grep weather

# Reiniciar servicio
sudo systemctl restart inkypi
```

### Problema: "Weather data not updating"

```bash
# Verificar conexión a internet
ping google.com

# Revisar si Open-Meteo API está disponible
curl -s "https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&daily=weathercode" | head -50

# Ver logs detallados
sudo journalctl -u inkypi -f
```

### Problema: "Image not rendering"

```bash
# Verificar que Chromium está instalado
which chromium-browser

# Si no, instalar:
sudo apt install chromium-browser

# Reintentar
sudo systemctl restart inkypi
```

### Problema: "Permission denied"

```bash
# Verificar permisos
ls -la src/plugins/weather_calendar/

# Si es necesario, cambiar permisos
sudo chown -R pi:pi /opt/inkypi/src/plugins/weather_calendar/
```

---

## 📊 Monitoreo Continuo

### Ver estado del plugin en tiempo real

```bash
# Mostrar últimas 50 líneas de logs
sudo journalctl -u inkypi -n 50

# Seguir logs en tiempo real
sudo journalctl -u inkypi -f

# Filtrar solo errores
sudo journalctl -u inkypi -p err -n 20
```

### Verificar uso de recursos

```bash
# Ver uso de CPU y memoria
ps aux | grep inkypi

# Ver procesos de Python
top -p $(pgrep -f "python.*inkypi")
```

### Programar actualización automática

```bash
# Editar crontab
sudo crontab -e

# Agregar línea para actualizar plugin cada día a las 2 AM:
0 2 * * * cd /opt/inkypi && git pull origin main && sudo systemctl restart inkypi
```

---

## 🎯 Configuraciones Recomendadas por Zona Horaria

| Región | Timezone | Time Format |
|--------|----------|------------|
| **España** | Europe/Madrid | 24h |
| **UK** | Europe/London | 24h |
| **USA - Nueva York** | America/New_York | 12h |
| **USA - Los Angeles** | America/Los_Angeles | 12h |
| **Sudamérica** | America/Buenos_Aires | 24h |
| **Asia - Tokio** | Asia/Tokyo | 24h |

---

## ✅ Checklist Final

- [ ] Raspberry Pi con InkyPi instalado
- [ ] Plugin weather_calendar en directorio correcto
- [ ] Dependencias instaladas (icalendar, recurring-ical-events)
- [ ] Servicio reiniciado
- [ ] Configuración completada (Lat/Lon/Units)
- [ ] Web UI accesible en http://raspberrypi.local:5000
- [ ] Plugin mostrando en lista de plugins
- [ ] Display mostrando imagen correcta
- [ ] Logs sin errores
- [ ] Calendario iCloud configurado (opcional)

---

## 📞 Soporte

Si encuentras problemas:

1. **Revisa los logs**: `sudo journalctl -u inkypi -f`
2. **Verifica conexión internet**: `ping google.com`
3. **Comprueba dependencies**: `pip list | grep -E "icalendar|recurring"`
4. **Reinicia el servicio**: `sudo systemctl restart inkypi`
5. **Consulta documentación**: `cat RESUMEN_FINAL.md` o `cat BUG_FIXES.md`

---

**Última actualización**: 6 Feb 2026  
**Estado**: ✅ Listo para Producción  
**Versión**: Weather Calendar Plugin v2.0
