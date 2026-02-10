# 🔧 Instalación Corregida - Cómo se resolvió

## El Problema

La Raspberry Pi tenía **dos instalaciones de InkyPi** ejecutándose simultáneamente:

1. **Instalación antigua** (con symlinks rotos):
   - Código en: `/home/pablojuanes/InkyPi/` (obsoleta)
   - Script: `/usr/local/bin/inkypi` → apuntaba aquí
   - Venv: `/usr/local/inkypi/venv_inkypi` → era un directorio viejo

2. **Instalación nueva** (con tu Weather Calendar):
   - Código en: `/opt/inkypi/` (actualizada desde GitHub)
   - No estaba conectada al servicio systemd

**Resultado**: El servicio ejecutaba el código antiguo, sin Weather Calendar.

---

## La Solución

### Paso 1: Actualizar symlinks

```bash
# En la Raspberry Pi (como root o con sudo)

# Apuntar /usr/local/inkypi/src al código nuevo
sudo rm /usr/local/inkypi/src
sudo ln -s /opt/inkypi/src /usr/local/inkypi/src

# Apuntar /usr/local/inkypi/venv_inkypi al venv nuevo
sudo rm -rf /usr/local/inkypi/venv_inkypi
sudo ln -s /opt/inkypi/venv /usr/local/inkypi/venv_inkypi
```

### Paso 2: Instalar dependencias

```bash
# Desde la Raspberry Pi
sudo bash -c 'source /opt/inkypi/venv/bin/activate && pip install -r /opt/inkypi/install/requirements.txt'
```

### Paso 3: Reiniciar el servicio

```bash
sudo systemctl restart inkypi
```

### Paso 4: Verificar

```bash
# Verificar que el servicio está corriendo desde /opt/inkypi
sudo systemctl status inkypi

# Deberías ver:
# Main PID: XXXXX (bash)
# └─XXXXX python -u /opt/inkypi/src/inkypi.py  ← ¡Aquí!
```

---

## ¿Por qué pasó esto?

Cuando instalaste InkyPi originalmente, la instalación se hizo en:
- `/home/pablojuanes/InkyPi/` (usando el instalador de InkyPi)
- Los symlinks en `/usr/local/inkypi/` apuntaban allí

Luego, cuando clonaste tu fork con Weather Calendar, fue a:
- `/opt/inkypi/` (siguiendo la documentación de DEPLOYMENT_OPTIONS.md)

Pero el servicio **no fue actualizado** para apuntar a la nueva ubicación.

---

## Cómo evitarlo en el futuro

### ✅ Opción A: Usar `/opt/inkypi` desde el principio (Recomendado)

Si instalas por primera vez, asegúrate de que la instalación original esté en `/opt/inkypi`:

```bash
# En la Raspberry Pi
cd /opt
sudo git clone https://github.com/TU-USUARIO/InkyPi.git inkypi
cd inkypi
sudo bash install/install.sh
```

### ✅ Opción B: Limpiar antes de reinstalar

Si tienes dos instalaciones, elimina la antigua:

```bash
# En la Raspberry Pi
# 1. Detén el servicio
sudo systemctl stop inkypi

# 2. Elimina la instalación antigua (si ya no la necesitas)
sudo rm -rf /home/pablojuanes/InkyPi

# 3. Asegúrate de que /opt/inkypi existe y tiene tu código
ls /opt/inkypi/src/plugins/weather_calendar/

# 4. Actualiza symlinks (ver Paso 1 arriba)

# 5. Reinicia
sudo systemctl restart inkypi
```

### ✅ Opción C: Usar la instalación existente en `/opt`

Si tu código ya está en `/opt/inkypi`, simplemente actualiza los symlinks (Paso 1).

---

## Verificación Final

Después de los cambios, deberías ver:

```bash
# 1. El servicio corre desde /opt/inkypi
sudo systemctl status inkypi
# → Main PID: python -u /opt/inkypi/src/inkypi.py

# 2. Weather Calendar está en el plugin registry
ls /opt/inkypi/src/plugins/weather_calendar/
# → weather_calendar.py, plugin-info.json, settings.html, render/

# 3. El web UI carga sin errores
# Abre http://raspberrypi.local:5000
# Deberías ver "Weather + Calendar" en la lista de plugins
```

---

## Resumen de cambios hechos el 10 Feb 2026

| Acción | Comando |
|--------|---------|
| Actualizar symlink src | `sudo rm /usr/local/inkypi/src && sudo ln -s /opt/inkypi/src /usr/local/inkypi/src` |
| Actualizar symlink venv | `sudo rm -rf /usr/local/inkypi/venv_inkypi && sudo ln -s /opt/inkypi/venv /usr/local/inkypi/venv_inkypi` |
| Instalar dependencias | `sudo bash -c 'source /opt/inkypi/venv/bin/activate && pip install -r /opt/inkypi/install/requirements.txt'` |
| Reiniciar servicio | `sudo systemctl restart inkypi` |

**Estado actual**: ✅ Servicio ejecutando desde `/opt/inkypi` con Weather Calendar plugin cargado.

---

**Última actualización**: 10 Feb 2026, 23:54 CET
