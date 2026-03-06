# Update Timestamp Feature

## Cambio Realizado

He añadido un **timestamp de actualización** al display que muestra exactamente cuándo fue la última vez que se actualizó.

## Cómo Funciona

### En el Display
En la **parte inferior** del Weather Calendar verás una línea pequeña que dice:

```
Updated: 03/06 02:15 PM
```

O en formato 24h (si lo tienes configurado):
```
Updated: 06/03 14:15
```

### Qué Significa
- **Cada vez que la pantalla se actualiza**, el timestamp se actualiza también
- Si ves que la fecha/hora **no cambia**, significa que la pantalla **no se está actualizando**
- Si ves que **sí cambia**, confirma que el sistema está funcionando

### Formato

El timestamp se adapta a tu configuración de `time_format`:

**12-hour format (AM/PM):**
```
MM/DD HH:MM AM/PM
Ejemplo: 03/06 02:15 PM
```

**24-hour format:**
```
DD/MM HH:MM
Ejemplo: 06/03 14:15
```

## Dónde Está

En el archivo HTML: `/Users/pablojuanes/Documents/InkyPi/src/plugins/weather_calendar/render/weather_calendar.html`

Línea final del display:
```html
<!-- Update Info -->
<div class="update-info">
    Updated: {{ last_update }}
</div>
```

### Estilos CSS
```css
.update-info {
    text-align: center;
    color: #000;
    font-weight: 600;
    font-size: 6px;            /* Pequeño para caber en 450x300 */
    margin-top: 8px;
    padding-top: 6px;
    border-top: 1px solid #000; /* Línea separadora */
    letter-spacing: 0.1px;
}
```

## En el Código Python

En `weather_calendar.py`, se calcula así:

```python
# Get current time for update timestamp
now = datetime.now(tz)
if time_format == "12h":
    last_update = now.strftime("%m/%d %I:%M %p")
else:
    last_update = now.strftime("%d/%m %H:%M")

# Pasar al template
template_params = {
    "weather": weather_info,
    "events": events_today,
    ...
    "last_update": last_update  # ← Aquí se pasa
}
```

## Cómo Verificar

### Test Inmediato

Fuerza una actualización:
```bash
ssh inkypi "curl -X POST http://localhost/update_now \
  -d 'plugin_id=weather_calendar' \
  -d 'latitude=40.7128' \
  -d 'longitude=-74.0060' \
  -d 'units=metric'"
```

Espera 30 segundos, luego:
1. Mira tu pantalla
2. **Nota la hora exacta** que aparece en "Updated"
3. Espera unos minutos
4. **Fuerza otra actualización** con el comando anterior
5. La hora debería haber **aumentado**

Si cambió = ✅ **El display se está actualizando correctamente**

### Test Automático (Próxima Hora)

El plugin tiene un refresh cada 1 hora (configurado en `device.json`).

En la próxima actualización automática, el timestamp también se actualizará.

## Commit de Referencia

- **6188b8e** - "feat: add last update timestamp to weather calendar display"

## Beneficios

✅ **Verificación visual** - Ves exactamente cuándo se actualizó  
✅ **Debugging** - Fácil saber si el sistema está funcionando  
✅ **Confianza** - Sabes que los datos son recientes  
✅ **Pequeño** - Font de 6px, no interfiere con el diseño  
✅ **Adaptable** - Respeta la configuración de time_format  

## Próximas Mejoras Posibles

Si quieres cambiar:
- **Tamaño del timestamp:** Edita `font-size: 6px` en `.update-info`
- **Formato de hora:** Modifica el `strftime` en `weather_calendar.py`
- **Ubicación:** Muévelo en el HTML (arriba, abajo, lado, etc.)
- **Estilo:** Cambia color, border, padding, etc. en CSS

## Estado

✅ Implementado  
✅ Pusheado a GitHub  
✅ Actualizado en Raspberry Pi  
✅ Servicio reiniciado  

**El timestamp está listo para usar. Mira tu pantalla en la próxima actualización.** 📦
