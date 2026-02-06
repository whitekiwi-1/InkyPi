# Testing the Weather + Calendar Plugin

## Quick Test (sin Hardware)

### 1. Instalar dependencias de desarrollo
```bash
cd /Users/pablojuanes/Documents/InkyPi
python3 -m venv venv
source venv/bin/activate
pip install -r install/requirements-dev.txt
```

### 2. Ejecutar en modo desarrollo
```bash
python src/inkypi.py --dev
```

Espera a ver:
```
Serving on http://localhost:8080
```

### 3. Acceder a la Web UI
- Abre en navegador: **http://localhost:8080**
- Ve a **Plugins** en la barra lateral
- Busca **"Weather + Calendar"**

### 4. Configurar el Plugin

Completa los campos:

```
Title: Mi Clima y Agenda
Latitude: 40.7128
Longitude: -74.0060
Units: Metric (°C)
iCloud Calendar URLs: (opcional - pega URL pública .ics si tienes)
```

### 5. Vista Previa
- Haz clic en botón **"Display"**
- Espera 5-10 segundos mientras procesa
- Deberías ver una vista previa de la imagen

### 6. Verificar Renderizado
La imagen se guarda en:
```
mock_display_output/latest.png
```

Abre este archivo para ver cómo se vería en el e-ink display.

---

## Troubleshooting

### ❌ Error: "ModuleNotFoundError: No module named 'X'"
**Solución**: Asegúrate que venv esté activado
```bash
source venv/bin/activate
pip install -r install/requirements-dev.txt
```

### ❌ Error en "Display" del plugin
**Solución**: Revisa la consola de terminal para el error exacto
```
python src/inkypi.py --dev
# Mira los logs de error en la terminal
```

### ❌ No aparece el plugin en la lista
**Solución**: El archivo `plugin-info.json` debe estar correctamente formateado
```bash
cat src/plugins/weather_calendar/plugin-info.json
# Debe mostrar:
# {
#     "display_name": "Weather + Calendar",
#     "id": "weather_calendar",
#     "class": "WeatherCalendar"
# }
```

### ❌ "Weather data not loading"
**Posibles causas:**
- Latitud/Longitud incorrecta
- Sin conexión a internet
- Open-Meteo API no disponible (raro)

**Solución**:
- Verifica coordenadas con Google Maps
- Prueba: `curl "https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&daily=temperature_2m_max,temperature_2m_min,weathercode&current_weather=true&timezone=auto&forecast_days=3"`

### ❌ "No events showing"
**Posibles causas:**
- URL de calendario incorrecta
- Calendario no es público en iCloud
- Sin eventos hoy

**Solución**:
1. Verifica que calendario esté compartido en iCloud.com
2. Prueba la URL en el navegador - debería descargar un archivo .ics
3. Verifica que haya eventos hoy en ese calendario

---

## Testing Completo (Con Cambios de Código)

Si quieres modificar el plugin:

### 1. Editar el código
```bash
# Edita por ejemplo: src/plugins/weather_calendar/weather_calendar.py
# O el template: src/plugins/weather_calendar/render/weather_calendar.html
```

### 2. Reload del plugin
El desarrollo actualmente requiere reiniciar el servidor:
```bash
# Presiona Ctrl+C en la terminal donde corre `python src/inkypi.py --dev`
# Luego ejecuta nuevamente:
python src/inkypi.py --dev
```

### 3. Probar cambios
- Abre nuevamente http://localhost:8080
- Ve a Weather + Calendar plugin
- Haz clic en "Display"
- Verifica cambios en `mock_display_output/latest.png`

---

## Debugging Avanzado

### Ver logs del plugin
En la terminal donde corre `python src/inkypi.py --dev`, verás logs como:
```
INFO: Saving image to /path/to/current_image.png
DEBUG: Rendering template weather_calendar.html
```

### Debuggear API calls
Añade temporalmente prints en `weather_calendar.py`:
```python
def get_open_meteo_data(self, lat, long):
    url = OPEN_METEO_FORECAST_URL.format(lat=lat, long=long)
    print(f"DEBUG: Fetching from {url}")  # ← Añade esto
    response = requests.get(url, timeout=10)
    print(f"DEBUG: Response status: {response.status_code}")  # ← Esto también
    return response.json()
```

### Inspeccionar JSON del calendario
```python
def fetch_calendar_events_today(self, calendar_urls, tz):
    for url in calendar_urls:
        response = requests.get(url.strip(), timeout=10)
        print(f"DEBUG Calendar response:\n{response.text[:500]}")  # Primeros 500 chars
```

---

## Casos de Uso para Probar

| Caso | Cómo Probar |
|------|-----------|
| **Sin calendario** | Deja URLs en blanco, solo muestra clima |
| **Con 1 calendario** | Pega 1 URL de iCloud |
| **Con N calendarios** | Pega múltiples URLs usando botón "+ Add Another Calendar" |
| **Cambio de unidades** | Cambia entre Celsius/Fahrenheit, haz Display |
| **Diferentes ubicaciones** | Cambia Lat/Long (ej: 51.5074, -0.1278 para Londres) |
| **Sin internet** | Desconecta WiFi, intenta Display → debería fallar gracefully |

---

## Performance Testing

El plugin debería renderizar en < 3 segundos.

Para medir:
```bash
# Añade esto en weather_calendar.py:
import time

def generate_image(self, settings, device_config):
    start = time.time()
    # ... resto del código ...
    elapsed = time.time() - start
    logger.info(f"Plugin render time: {elapsed:.2f}s")
```

---

## Revertir Cambios

Si hay problemas, revierte a la versión anterior:
```bash
# Ver todas las ramas
git branch

# Ir a backup
git checkout backup-20260206

# Volver a main
git checkout main
```

---

**¿Necesitas ayuda?** Revisa los logs en la terminal - InkyPi es muy detallista con los errores.
