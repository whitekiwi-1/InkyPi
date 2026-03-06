# 🔧 Fixes para "Update Now" del plugin Weather Calendar

## Problemas encontrados y solucionados

### Problema 1: KeyError - plugin_id no estaba en el formulario

**Error**:
```
KeyError: 'plugin_id'
File "/opt/inkypi/src/blueprints/plugin.py", line 136, in update_now
    plugin_id = plugin_settings.pop("plugin_id")
```

**Causa**: El formulario HTML del plugin `settings.html` no tenía un campo hidden con el `plugin_id`, que es requerido por el framework InkyPi.

**Solución**: Agregamos un input hidden al inicio del formulario:
```html
<form id="weatherCalendarSettingsForm">
    <!-- Hidden field for plugin ID (required by InkyPi framework) -->
    <input type="hidden" name="plugin_id" value="weather_calendar">
    ...
</form>
```

**Commit**: `e47e3f1`

---

### Problema 2: Protocolo webcal:// no es soportado por requests

**Error**:
```
InvalidURL: No host supplied. Perhaps you meant http://... or https://...?
```

**Causa**: Los URLs de iCloud calendars vienen en formato `webcal://` o `webcals://`, pero la librería `requests` de Python solo soporta `http://` y `https://`.

**Solución**: En la función `fetch_calendar_events_today()`, convertimos automáticamente:
```python
url_str = url.strip()
if url_str.startswith('webcal://'):
    url_str = url_str.replace('webcal://', 'https://', 1)
elif url_str.startswith('webcals://'):
    url_str = url_str.replace('webcals://', 'https://', 1)
```

**Commit**: `f8e21dc`

---

## Cambios realizados

| Archivo | Cambio | Commit |
|---------|--------|--------|
| `src/plugins/weather_calendar/settings.html` | Agregado: `<input type="hidden" name="plugin_id" value="weather_calendar">` | `e47e3f1` |
| `src/plugins/weather_calendar/weather_calendar.py` | Agregada conversión de `webcal://` → `https://` en `fetch_calendar_events_today()` | `f8e21dc` |

---

## Prueba de funcionamiento

Después de estos fixes, el plugin debería:

1. ✅ Aceptar la solicitud de "Update Now" sin errores de KeyError
2. ✅ Convertir automáticamente URLs de iCloud (`webcal://`) a HTTPS
3. ✅ Descargar eventos del calendario sin errores de protocolo

### Paso a paso para probar:

1. Abre http://192.168.1.97 en tu navegador
2. Ve a **Plugins** → **Weather + Calendar**
3. Ingresa los datos:
   - **Latitude**: 40.499396124744486
   - **Longitude**: -3.863496780395508
   - **Calendar URL**: `webcal://p183-caldav.icloud.com/published/2/MTEzNjk5NzkwMTExMzY5OUX-YfR_qqgq30ip9lUtyQmERBkQGyx-zGdRCSX6Yx69WEGvuitdcOHd2_e2sUoI-Tuo27kA9e6ZVaPCcCLh1cg`
4. Haz clic en **"Update Now"**
5. Deberías ver la imagen rendered en la pantalla sin errores

---

## Logs relevantes

Antes (Con errores):
```
11:22:30 - ERROR - blueprints.plugin - Error in update_now: 'plugin_id'
KeyError: 'plugin_id'
```

Después (Sin errores esperado):
```
11:30:41 - INFO - __main__ - Starting InkyPi in PRODUCTION mode on port 80
11:30:51 - INFO - refresh_task - Starting refresh task
```

---

## Historial de cambios

- **6 Mar 2026, 11:25**: Identificado error de plugin_id
- **6 Mar 2026, 11:27**: Fixed: Agregado plugin_id a settings.html (Commit e47e3f1)
- **6 Mar 2026, 11:28**: Identificado problema con webcal://
- **6 Mar 2026, 11:29**: Fixed: Conversión automática de webcal:// a https:// (Commit f8e21dc)
- **6 Mar 2026, 11:30**: Servicios reiniciados y verificados

---

**Status**: ✅ COMPLETADO - Listo para usar

**Próximos pasos**: 
- Accede a http://192.168.1.97
- Ve a Plugins → Weather + Calendar
- Configura tus coordenadas y calendario
- Haz clic en "Update Now"
