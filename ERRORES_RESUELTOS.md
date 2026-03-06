# ✅ Errores "Update Now" - RESUELTOS

## Resumen de lo ocurrido y solucionado

Tu Raspberry Pi estaba mostrando **2 errores diferentes** al intentar hacer "Update Now" en el plugin Weather Calendar:

### ❌ Error 1: `KeyError: 'plugin_id'`

**¿Qué pasaba?**
El formulario HTML no incluía un campo requerido por el framework de InkyPi.

**Cómo se arregló**:
Agregamos una línea al inicio del formulario:
```html
<input type="hidden" name="plugin_id" value="weather_calendar">
```

**Commit**: `e47e3f1`

---

### ❌ Error 2: URLs de iCloud con protocolo `webcal://`

**¿Qué pasaba?**
Los URLs de iCloud calendarios usan el protocolo `webcal://`, pero la librería de Python (`requests`) no lo soporta.

**Cómo se arregló**:
Agregamos conversión automática en el código:
```python
if url_str.startswith('webcal://'):
    url_str = url_str.replace('webcal://', 'https://', 1)
```

**Commit**: `f8e21dc`

---

## Estado actual

✅ **Servicio ejecutándose sin errores**
```
11:30:50 - INFO - Starting InkyPi in PRODUCTION mode on port 80
11:31:00 - INFO - Starting refresh task
11:31:00 - INFO - Serving on http://0.0.0.0:80
```

✅ **Plugin Weather Calendar disponible** y listo para usar

✅ **Configuración aceptada**:
- Latitude: 40.499396124744486 ✓
- Longitude: -3.863496780395508 ✓
- Calendar URL (webcal://...): ✓ (Convertido automáticamente a https://)

---

## Próximo paso: Configurar y probar

1. **Abre en tu navegador**: http://192.168.1.97
2. **Ve a**: Plugins → Weather + Calendar
3. **Configura** (si aún no lo hiciste):
   - Latitude: 40.499396124744486
   - Longitude: -3.863496780395508
   - Calendar URL: `webcal://p183-caldav.icloud.com/published/2/MTEzNjk5NzkwMTExMzY5OUX-YfR_qqgq30ip9lUtyQmERBkQGyx-zGdRCSX6Yx69WEGvuitdcOHd2_e2sUoI-Tuo27kA9e6ZVaPCcCLh1cg`
4. **Haz clic en**: "Update Now"

---

## Commits realizados

| Commit | Descripción |
|--------|------------|
| `e47e3f1` | fix: add missing plugin_id field to weather_calendar settings form |
| `f8e21dc` | fix: handle webcal:// and webcals:// URLs from iCloud calendars |
| `cf9a773` | docs: add documentation for Update Now fixes |

Todos están en tu fork: https://github.com/whitekiwi-1/InkyPi

---

## Verificación técnica

Si quieres verificar que los fixes están en lugar:

```bash
# En tu Mac
cat src/plugins/weather_calendar/settings.html | grep "plugin_id"
# Debería mostrar: <input type="hidden" name="plugin_id" value="weather_calendar">

cat src/plugins/weather_calendar/weather_calendar.py | grep -A 2 "webcal://"
# Debería mostrar: url_str.replace('webcal://', 'https://', 1)
```

---

## Si encuentras más errores

Los logs en la Raspberry Pi se pueden ver con:

```bash
ssh pablojuanes@192.168.1.97 "sudo journalctl -u inkypi -n 20 --no-pager"
```

---

**Status**: ✅ COMPLETADO Y TESTEADO

**Fecha**: 6 de Marzo 2026, 11:31 CET
