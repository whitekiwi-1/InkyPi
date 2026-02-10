# ✅ Problema Resuelto - Dos versiones de InkyPi en la Raspberry Pi

## Lo que estaba pasando

Tu Raspberry Pi en **192.168.1.97** tenía dos instalaciones de InkyPi:

### Instalación 1: La ANTIGUA (la que estaba corriendo)
- Ubicación: `/home/pablojuanes/InkyPi/`
- Servicio: `/usr/local/bin/inkypi` → apuntaba aquí
- Problema: **No tenía el plugin Weather Calendar**

### Instalación 2: La NUEVA (la que acabamos de crear)
- Ubicación: `/opt/inkypi/`
- Con: **Weather Calendar plugin completo**
- Problema: **El servicio no estaba usando esta**

---

## Cómo se resolvió

### 1️⃣ Se actualizaron los symlinks

El servicio en `/usr/local/inkypi/` tenía dos symlinks:
- `src` → apuntaba a `/home/pablojuanes/InkyPi/src` (VIEJO)
- `venv_inkypi` → era un directorio antiguo (VIEJO)

Los cambiamos para que apunten a `/opt/inkypi/`:

```bash
# Actualizar symlink de código
sudo rm /usr/local/inkypi/src
sudo ln -s /opt/inkypi/src /usr/local/inkypi/src

# Actualizar symlink de entorno virtual
sudo rm -rf /usr/local/inkypi/venv_inkypi
sudo ln -s /opt/inkypi/venv /usr/local/inkypi/venv_inkypi
```

### 2️⃣ Se instalaron dependencias

```bash
sudo bash -c 'source /opt/inkypi/venv/bin/activate && pip install -r /opt/inkypi/install/requirements.txt'
```

### 3️⃣ Se reinició el servicio

```bash
sudo systemctl restart inkypi
```

---

## Estado ACTUAL ✅

```
✅ Servicio ejecutando desde: /opt/inkypi/src/inkypi.py
✅ Plugin Weather Calendar: CARGADO
✅ Servidor web: EJECUTÁNDOSE en puerto 80
✅ Refresh task: INICIADA
```

### Verificación:

```bash
# En la Raspberry Pi
sudo systemctl status inkypi

# Deberías ver:
# Active: active (running) since...
# Main PID: XXXXX (python -u /opt/inkypi/src/inkypi.py)
```

---

## Siguiente: Configurar el plugin

Ahora que el servicio está corriendo con tu código, puedes configurar Weather Calendar:

1. Abre: **http://192.168.1.97** en tu navegador
2. Ve a **Plugins** → **Weather + Calendar**
3. Configura:
   - **Latitude**: Tu latitud (ej: 39.4699)
   - **Longitude**: Tu longitud (ej: -0.3763)
   - **Units**: Métrico o Imperial
   - **Calendar URLs**: URLs de tus calendarios iCloud (opcional)
4. Haz click en **Save**

---

## Commits realizados

| Commit | Descripción |
|--------|-----------|
| `dd0d637` | fix: update GitHub fork URL to correct capitalization |
| `0104834` | docs: add installation fix guide for dual InkyPi installations |

Ambos ya están en tu fork en GitHub: https://github.com/whitekiwi-1/InkyPi

---

## Resumen de archivos añadidos

- ✅ `INSTALLATION_FIXED.md` - Guía completa de la solución

---

## Si en el futuro ocurre algo similar...

Simplemente ejecuta estos 3 comandos en la Raspberry Pi:

```bash
# 1. Actualizar symlinks
sudo rm /usr/local/inkypi/src && sudo ln -s /opt/inkypi/src /usr/local/inkypi/src
sudo rm -rf /usr/local/inkypi/venv_inkypi && sudo ln -s /opt/inkypi/venv /usr/local/inkypi/venv_inkypi

# 2. Instalar dependencias
sudo bash -c 'source /opt/inkypi/venv/bin/activate && pip install -r /opt/inkypi/install/requirements.txt'

# 3. Reiniciar
sudo systemctl restart inkypi
```

O simplemente ejecuta en SSH:

```bash
ssh pablojuanes@192.168.1.97 "bash /opt/inkypi/install/install.sh"
```

---

**Fecha**: 10 de Febrero 2026, 23:54 CET
**Status**: ✅ RESUELTO - InkyPi corriendo con Weather Calendar
