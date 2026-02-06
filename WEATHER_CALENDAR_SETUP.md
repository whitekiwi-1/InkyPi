# Weather + Calendar Plugin - Setup Guide

## What's New

Un nuevo plugin **Weather + Calendar** ha sido creado. Este plugin combina:
- **Pronóstico de 3 días** (hoy + próximos 2 días)
- **Eventos de iCloud Calendar** para hoy

## Ubicación del Plugin

```
src/plugins/weather_calendar/
├── weather_calendar.py        # Lógica principal del plugin
├── plugin-info.json          # Metadata del plugin
├── settings.html             # UI de configuración
├── icon.png                  # Icono del plugin
├── README.md                 # Documentación detallada
└── render/
    ├── weather_calendar.html # Template HTML
    └── weather_calendar.css  # Estilos CSS
```

## Configuración Rápida

### 1. Obtener coordenadas de tu ubicación

Ve a Google Maps, busca tu dirección, haz clic derecho → Coordenadas
Ejemplo: Nueva York → Lat: 40.7128, Lon: -74.0060

### 2. Obtener URLs de iCloud Calendar (opcional)

1. Ve a **iCloud.com** → **Calendario**
2. Haz clic derecho en un calendario → **Compartir configuración**
3. Activa "Compartir calendario"
4. Copia el enlace **"Calendario público"** (termina en `.ics`)

**Ejemplo:**
```
https://p12-caldav.icloud.com/published/2/MTMyODc5NzYyODI3NzIxMjM3MDc1Nzk0OTE0NzkyNTE1/calendar.ics
```

### 3. Configurar en InkyPi

1. Abre http://localhost:8080 (o tu InkyPi web UI)
2. Ve a **Plugins** → **Weather + Calendar**
3. Llena los campos:
   - **Título**: "Mi Clima y Eventos"
   - **Latitud**: 40.7128
   - **Longitud**: -74.0060
   - **Unidades**: Celsius o Fahrenheit
   - **URLs de Calendario iCloud**: (pega tus URLs)
4. Haz clic en **"Display"** para ver vista previa
5. Haz clic en **"Save Settings"** para guardar

## Características

✅ **API de Clima Gratuita** - Open-Meteo (sin necesidad de API key)
✅ **Múltiples Calendarios** - Soporta varios calendarios iCloud
✅ **Sin Dependencias Externas** - Usa las librerías existentes de InkyPi
✅ **Responsive** - Se adapta a diferentes tamaños de pantalla

## Datos Que Muestra

### Pronóstico (3 días)
- Fecha del día
- Condición del clima (Despejado, Nublado, Lluvia, etc.)
- Temperatura máxima y mínima

### Eventos de Hoy
- Hora del evento
- Título del evento
- Eventos de todo el día marcados como "All day"

## APIs Usadas

| API | Propósito | Costo |
|-----|----------|-------|
| **Open-Meteo** | Pronóstico de clima | Gratis |
| **iCloud Calendar** | Eventos del calendario | Gratis (requiere compartir) |

## Solución de Problemas

### ❌ "No events showing"
- Verifica que el calendario esté compartido públicamente en iCloud
- Comprueba que la URL es correcta (debe terminar en `.ics`)
- Asegúrate de que hay eventos hoy en ese calendario

### ❌ "Weather data not loading"
- Verifica que la Latitud y Longitud sean correctas
- Comprueba la conexión de red
- Open-Meteo es muy confiable, pero puedes verificar su estado en: https://status.open-meteo.com/

### ❌ "Display looks truncated"
- Ajusta los tamaños de fuente en `render/weather_calendar.css`
- Reduce el número de calendarios o la longitud del título

## Desarrollo Futuro

Posibles mejoras:
- [ ] Soporte para Google Calendar
- [ ] Modo oscuro
- [ ] Iconos de clima animados
- [ ] Notificaciones de eventos próximos
- [ ] Integración con API de calidad del aire

## Revertir a Versión Anterior

Si hay problemas, puedes volver a la versión anterior de InkyPi:
```bash
git checkout backup-20260206
```

---

**¿Preguntas?** Revisa `src/plugins/weather_calendar/README.md` para más detalles.
