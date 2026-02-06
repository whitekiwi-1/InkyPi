# 🚀 QUICK START - Llevar Weather Calendar Plugin a Raspberry Pi

**En 5 minutos** - Guía simplificada paso a paso

---

## ⚡ TL;DR (Si tienes InkyPi ya instalado)

```bash
# 1. Conectarse por SSH
ssh pi@raspberrypi.local

# 2. Actualizar código
cd /opt/inkypi
sudo git pull origin main

# 3. Instalar nuevas dependencias
source venv/bin/activate
pip install icalendar recurring-ical-events
deactivate

# 4. Reiniciar
sudo systemctl restart inkypi

# 5. Configurar en web UI
open http://raspberrypi.local:5000
# Plugins → Weather + Calendar → Settings
# Ingresa: Latitude, Longitude, Units
# Click: Display
```

---

## 📋 Opción A: Tienes InkyPi instalado

### 1️⃣ SSH a la Pi

```bash
ssh pi@raspberrypi.local
```

Si no funciona, usa la IP directa:
```bash
ssh pi@192.168.1.YOUR_PI_IP
```

### 2️⃣ Actualizar el código

```bash
cd /opt/inkypi
sudo git pull origin main
```

### 3️⃣ Instalar dependencias nuevas

```bash
source venv/bin/activate
pip install icalendar recurring-ical-events
deactivate
```

### 4️⃣ Reiniciar InkyPi

```bash
sudo systemctl restart inkypi

# Verificar que está corriendo
sudo systemctl status inkypi

# Ver logs en tiempo real (Ctrl+C para salir)
sudo journalctl -u inkypi -f
```

---

## 📋 Opción B: Instalación Limpia (Sin InkyPi previo)

### ⚠️ IMPORTANTE: Antes de empezar

Este guide instala **TU VERSIÓN CON WEATHER CALENDAR**, no la versión original de InkyPi.

**Tienes 3 opciones:**

1. **Subir a GitHub** (Recomendado)
   - Fork el repo de fatihak/inkypi
   - Push tus cambios a tu fork
   - En Paso 2, clona tu fork

2. **Usar directo desde tu máquina**
   - Copia el directorio completo a la Pi
   - En Paso 2, usa `scp` en lugar de `git clone`

3. **Subir a un servidor privado**
   - Hostea tu propio repo Git
   - Clona desde ahí

**En esta guía usaremos Opción 1** (GitHub). Si prefieres otra, salta a la nota en Paso 2.

---

### Paso 1: Preparar Pi

```bash
# Conectarse
ssh pi@raspberrypi.local

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3 python3-pip python3-venv git chromium-browser
```

### Paso 2: Clonar InkyPi (Tu versión con Weather Calendar)

```bash
cd /opt
# ⚠️ IMPORTANTE: Reemplaza 'tu-usuario' con tu usuario de GitHub
sudo git clone https://github.com/tu-usuario/inkypi.git
cd inkypi

# O si es un fork local (sin publicar en GitHub):
# Copia el directorio directamente:
# sudo cp -r ~/Documents/InkyPi /opt/inkypi
# cd /opt/inkypi
```

**Notas:**
- Si tienes el código en GitHub, usa tu URL de fork
- Si es local, cópialo directamente como se muestra arriba
- Asegúrate de que **Weather Calendar plugin** esté en `src/plugins/weather_calendar/`
- Verifica con: `ls src/plugins/weather_calendar/`

### Paso 3: Setup

```bash
# Crear venv
sudo python3 -m venv venv
source venv/bin/activate

# Instalar
sudo pip install -r install/requirements-dev.txt

# Salir venv
deactivate

# Copiar archivos del servicio
sudo cp install/inkypi.service /etc/systemd/system/
sudo cp install/inkypi /usr/local/bin/
sudo chmod +x /usr/local/bin/inkypi

# Habilitar e iniciar
sudo systemctl daemon-reload
sudo systemctl enable inkypi
sudo systemctl start inkypi
```

---

## ⚙️ CONFIGURAR PLUGIN

### Opción 1: Web UI (Fácil)

```bash
# En tu computadora, abre:
http://raspberrypi.local:5000

# O usa la IP:
# http://192.168.1.100:5000
```

Luego:
1. Click en **Plugins**
2. Busca **Weather + Calendar**
3. Click en **Settings**
4. Completa:
   - **Latitude**: tu latitud (ej: 40.7128)
   - **Longitude**: tu longitud (ej: -74.0060)
   - **Units**: `metric` (°C) o `imperial` (°F)
   - **Calendar URLs**: (opcional, para eventos)
5. Click **Save**
6. Click **Display** para ver preview

### Opción 2: SSH (Manual)

```bash
# Editar configuración
sudo nano /opt/inkypi/src/plugins/weather_calendar/config.json
```

Pegar:
```json
{
    "latitude": "40.7128",
    "longitude": "-74.0060",
    "units": "metric",
    "calendarURLs[]": []
}
```

Guardar: `Ctrl+O`, Enter, `Ctrl+X`

Reiniciar: `sudo systemctl restart inkypi`

---

## 🔍 VERIFICAR QUE FUNCIONA

### Ver logs

```bash
sudo journalctl -u inkypi -f
```

Deberías ver:
```
INFO - Initializing Weather Calendar plugin
INFO - Fetching weather from Open-Meteo API
INFO - Rendering image: 800x480
INFO - Image updated successfully
```

### Ver imagen generada

```bash
# Descargar imagen a tu Mac
scp pi@raspberrypi.local:/opt/inkypi/src/static/images/current_image.png ~/Downloads/weather_display.png

# Luego abre ~/Downloads/weather_display.png en Preview
```

---

## 📍 ENCONTRAR TUS COORDENADAS

1. Abre https://www.google.com/maps
2. Busca tu ubicación
3. Click derecho → "¿Qué hay aquí?"
4. Copiar latitud/longitud

**Ejemplos:**
- Nueva York: 40.7128, -74.0060
- Madrid: 40.4168, -3.7038
- Londres: 51.5074, -0.1278
- Tokio: 35.6762, 139.6503

---

## 📅 AGREGAR CALENDARIO (Opcional)

Si quieres ver eventos de hoy en la pantalla:

### 1. Obtener URL de iCloud Calendar

1. Abre https://www.icloud.com
2. Inicia sesión
3. Abre **Calendar**
4. Click derecho en tu calendario → **Share Calendar**
5. Marca **Public Calendar**
6. Copia el URL público

### 2. Agregar a InkyPi

En web UI:
- Plugins → Weather + Calendar → Settings
- Pega URL en "Calendar URLs"
- Click "Add Calendar" (si quieres más)
- Click **Save**

---

## 🆘 PROBLEMAS COMUNES

### "No puedo conectar por SSH"

```bash
# Encontrar IP de la Pi
# En la Pi o router:
hostname -I

# Luego usa:
ssh pi@192.168.1.XXX
```

### "Plugin no aparece en la lista"

```bash
# Verificar que existe
ssh pi@raspberrypi.local
ls -la /opt/inkypi/src/plugins/weather_calendar/

# Reiniciar
sudo systemctl restart inkypi
```

### "Weather no se actualiza"

```bash
# Ver logs de error
sudo journalctl -u inkypi -n 50

# Verificar internet
ping google.com

# Probar API directamente
curl https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060
```

### "Imagen no se ve"

```bash
# Verificar Chromium instalado
which chromium-browser

# Si no, instalar:
sudo apt install chromium-browser

# Reiniciar:
sudo systemctl restart inkypi
```

---

## 📱 MONITOREAR EN TIEMPO REAL

```bash
# Ver logs continuos (Ctrl+C para salir)
sudo journalctl -u inkypi -f

# Ver solo últimas 20 líneas
sudo journalctl -u inkypi -n 20

# Ver solo errores
sudo journalctl -u inkypi -p err
```

---

## ✅ CHECKLIST

- [ ] SSH conectado a Pi
- [ ] Código actualizado (`git pull`)
- [ ] Dependencias instaladas
- [ ] InkyPi reiniciado
- [ ] Web UI accesible
- [ ] Plugin visible en lista
- [ ] Latitud/Longitud configuradas
- [ ] Units seleccionadas
- [ ] Display muestra imagen
- [ ] Logs sin errores

---

## 🎯 Próximos Pasos

Una vez funcionando:

1. **Ajusta el intervalo de refresh** en settings si es necesario
2. **Agrega calendario iCloud** si tienes eventos importantes
3. **Personaliza zona horaria** en device.json si es diferente
4. **Configura múltiples plugins** con rotación

---

## 📞 REFERENCIA RÁPIDA

| Comando | Propósito |
|---------|-----------|
| `ssh pi@raspberrypi.local` | Conectarse a Pi |
| `sudo systemctl status inkypi` | Ver estado |
| `sudo systemctl restart inkypi` | Reiniciar servicio |
| `sudo journalctl -u inkypi -f` | Ver logs en vivo |
| `sudo systemctl stop inkypi` | Detener servicio |
| `sudo systemctl start inkypi` | Iniciar servicio |

---

**¡Listo!** 🎉 Tu Weather Calendar plugin debería estar funcionando en la Pi.

Si tienes problemas, revisa `DEPLOYMENT_GUIDE.md` para más detalles.

Última actualización: 6 Feb 2026
