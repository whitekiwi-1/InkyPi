# 🔄 CÓMO USAR TU VERSIÓN CON WEATHER CALENDAR

Tienes 3 opciones para llevar tu código a la Raspberry Pi:

---

## Opción 1: GitHub (Recomendado) ⭐

### Paso 1: Crear un fork en GitHub

1. Abre https://github.com/fatihak/inkypi
2. Click **Fork** (esquina superior derecha)
3. Elige tu usuario como destino
4. Espera a que termine

### Paso 2: Push de tus cambios locales

En tu Mac, desde el directorio `/Users/pablojuanes/Documents/InkyPi`:

```bash
# Agregar remote a tu fork
git remote add mi-fork https://github.com/TU-USUARIO/inkypi.git

# Push al branch main de tu fork
git push mi-fork main

# O si quieres un branch diferente:
git push mi-fork weather-calendar
```

**¿Dónde está TU-USUARIO?** En https://github.com/settings/profile

### Paso 3: En la Raspberry Pi

```bash
cd /opt
sudo git clone https://github.com/TU-USUARIO/inkypi.git
cd inkypi
```

Reemplaza `TU-USUARIO` con tu usuario de GitHub.

### Verificar que tiene Weather Calendar

```bash
ls -la src/plugins/weather_calendar/
# Deberías ver: weather_calendar.py, plugin-info.json, render/, etc
```

---

## Opción 2: Copiar directo (Rápido) ⚡

Si no quieres usar GitHub, copia el directorio directamente:

### Paso 1: En tu Mac

```bash
# Asegúrate de que el código está en buen estado
cd /Users/pablojuanes/Documents/InkyPi
git status  # Debe estar clean (sin cambios sin commitear)

# Comprime el directorio
cd /Users/pablojuanes/Documents
tar czf inkypi-weather-calendar.tar.gz InkyPi/
```

### Paso 2: Transfiere a la Pi

```bash
# Desde tu Mac
scp /Users/pablojuanes/Documents/inkypi-weather-calendar.tar.gz pi@raspberrypi.local:~/

# Luego, en la Pi (SSH)
ssh pi@raspberrypi.local

# Descomprime
cd ~
tar xzf inkypi-weather-calendar.tar.gz

# Muévelo a /opt
sudo mv InkyPi /opt/inkypi
cd /opt/inkypi
```

### Paso 3: Continúa desde Paso 3 de QUICK_START.md

```bash
# Crear venv
sudo python3 -m venv venv
source venv/bin/activate
# ... resto de QUICK_START.md
```

### Verificar

```bash
ls -la src/plugins/weather_calendar/
```

---

## Opción 3: Servidor Git Privado (Avanzado)

Si tienes un servidor Git privado (GitLab, Gitea, etc):

```bash
# En tu Mac
git remote add servidor https://tu-servidor.com/repo.git
git push servidor main

# En la Pi
cd /opt
sudo git clone https://tu-servidor.com/repo.git inkypi
cd inkypi
```

---

## ¿Cuál elegir?

| Opción | Ventajas | Desventajas |
|--------|----------|------------|
| **GitHub** | Fácil de mantener, público, colaboración | Requiere cuenta GitHub |
| **Copia directa** | Funciona sin internet, sin cuenta | No se puede actualizar fácilmente |
| **Servidor privado** | Privado, control total | Requiere infraestructura |

**Recomendación**: Usa **Opción 1 (GitHub)** si piensas hacer actualizaciones futuras.

---

## ✅ Verificar que está correctamente instalado

```bash
# SSH a la Pi
ssh pi@raspberrypi.local

# Verificar plugin existe
ls -la /opt/inkypi/src/plugins/weather_calendar/

# Deberías ver:
# -rw-r--r--  weather_calendar.py
# -rw-r--r--  plugin-info.json
# -rw-r--r--  settings.html
# -rw-r--r--  icon.png
# drwxr-xr-x  render/

# Ver que render/ tiene el HTML
ls -la /opt/inkypi/src/plugins/weather_calendar/render/

# Deberías ver:
# -rw-r--r--  weather_calendar.html
```

---

## 🔄 Actualizar en el futuro (si usas GitHub)

```bash
# En la Pi
cd /opt/inkypi
sudo git pull mi-fork main

# Instalar nuevas dependencias
source venv/bin/activate
pip install -r install/requirements-dev.txt
deactivate

# Reiniciar
sudo systemctl restart inkypi
```

---

## 🆘 Troubleshooting

### "Git clone falla"

```bash
# Verificar conectividad
ping github.com

# Verificar credenciales (si es privado)
git config credential.helper osxkeychain
```

### "Plugin no aparece después de copiar"

```bash
# Verificar que está en el lugar correcto
ls -la /opt/inkypi/src/plugins/weather_calendar/

# Si no, estás en el directorio equivocado
# Asegúrate de que clonaste en /opt/inkypi, no en otro lado

# Reinicia después de copiar
sudo systemctl restart inkypi
```

### "Errores de dependencias después de copiar"

```bash
# Reinstala dependencias
source /opt/inkypi/venv/bin/activate
pip install -r /opt/inkypi/install/requirements-dev.txt
deactivate

# Reinicia
sudo systemctl restart inkypi
```

---

## 📋 Checklist

- [ ] Elegiste tu opción (GitHub, copiar, o servidor)
- [ ] El código está en `/opt/inkypi/` en la Pi
- [ ] Weather Calendar plugin existe: `ls src/plugins/weather_calendar/`
- [ ] `render/weather_calendar.html` existe
- [ ] Dependencias instaladas
- [ ] InkyPi reiniciado
- [ ] Plugin aparece en web UI

---

**Última actualización**: 6 Feb 2026
