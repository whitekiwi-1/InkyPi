# Weather + Calendar Plugin — Visual Preview

## 📺 Cómo se vería en la pantalla e-ink

### Layout General

La pantalla se divide en **2 secciones principales**:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃      MI CLIMA & AGENDA                 ┃  ← Título personalizable
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                         ┃
┃  Pronóstico 3 Días                      ┃
┃ ┌────────────┬────────────┬─────────┐   ┃
┃ │ 6 FEB      │ 7 FEB      │ 8 FEB   │   ┃
┃ │ (Hoy)      │ (Mañana)   │ (Vier)  │   ┃
┃ │            │            │         │   ┃
┃ │ Parcialmte │ Lluvia     │ Nublado │   ┃
┃ │ Nublado    │ Ligera     │         │   ┃
┃ │            │            │         │   ┃
┃ │ 22°C/15°C  │ 18°C/10°C  │20°C/12°C│   ┃
┃ └────────────┴────────────┴─────────┘   ┃
┃                                         ┃  ← 45% de pantalla
┃                                         ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                         ┃
┃  Eventos de Hoy                         ┃
┃  • 09:00    Standup del Equipo          ┃
┃  • 10:30    Revisión Proyecto InkyPi    ┃
┃  • 14:00    Reunión General Empresa     ┃
┃  • All day  Cumpleaños de María         ┃
┃                                         ┃
┃                                         ┃  ← 45% de pantalla
┃                                         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## 🎨 Elementos Visuales

### 1️⃣ Título Superior
- **Fuente**: Arial Bold, 32px
- **Estilo**: Centrado, línea debajo
- **Uso**: Muestra el título configurado por el usuario

### 2️⃣ Tarjetas de Pronóstico (Grid 3x1)
```
┌──────────────────────────────────────────┐
│ TARJETA DE PRONÓSTICO                    │
├──────────────────────────────────────────┤
│                                          │
│  Fecha: "6 FEB"          (16px Bold)     │
│  Día: "Hoy"              (14px Normal)   │
│                                          │
│  Condición: "Parcialmente Nublado"       │
│             (15px, centrado)             │
│                                          │
│  Temperaturas:                           │
│  Max: 22°C (Rojo)                        │
│  Min: 15°C (Azul)                        │
│                                          │
└──────────────────────────────────────────┘
```

**Características**:
- Bordes negros sólidos (2px)
- Fondo gris claro (#f5f5f5)
- Espaciado uniforme
- Se adapta a cualquier tamaño

### 3️⃣ Lista de Eventos
```
┌──────────────────────────────────────────┐
│ EVENTO                                   │
├──────────────────────────────────────────┤
│                                          │
│ ■ 09:00      Standup del Equipo          │
│   │                                      │
│   ├─ Hora: Arial Bold 14px, Azul         │
│   └─ Título: Arial Normal 15px           │
│                                          │
│ ■ 10:30      Revisión de Proyecto        │
│                                          │
│ ■ 14:00      Reunión General             │
│                                          │
│ ■ All day    Cumpleaños María            │
│                                          │
└──────────────────────────────────────────┘
```

**Características**:
- Línea azul vertical izquierda (4px)
- Cada evento en su propia línea
- Hora alineada a la izquierda (80px min width)
- Título ocupa resto de espacio
- Fondo suave (#f9f9f9)

## 🎯 Proporciones

| Elemento | % Pantalla | Notas |
|----------|-----------|-------|
| Título | 10% | Centrado, margen inferior |
| Pronóstico | 45% | 3 tarjetas lado a lado |
| Separador | 5% | Línea gris |
| Eventos | 40% | Lista flexible |

## 📱 Adaptación por Tamaño de Pantalla

### Pantalla 4" (600x448px)
```
┌──────────────────────────┐
│ MI CLIMA & AGENDA        │
├──────────────────────────┤
│ Pronóstico 3 Días        │
│ ┌──────────────────────┐ │
│ │ 6 FEB - Parcialmte   │ │
│ │ Nublado 22°C / 15°C  │ │
│ └──────────────────────┘ │
│ ┌──────────────────────┐ │
│ │ 7 FEB - Lluvia       │ │
│ │ Ligera 18°C / 10°C   │ │
│ └──────────────────────┘ │
│ ┌──────────────────────┐ │
│ │ 8 FEB - Nublado      │ │
│ │ 20°C / 12°C          │ │
│ └──────────────────────┘ │
├──────────────────────────┤
│ Eventos de Hoy           │
│ • 09:00 Standup          │
│ • 10:30 Revisión         │
│ • 14:00 Reunión          │
└──────────────────────────┘
```
**Cambios**: 1 tarjeta por fila (stack vertical)

### Pantalla 7.3" (1024x768px) - ACTUAL
```
[Ver ejemplo arriba]
3 tarjetas lado a lado
Todos los eventos visibles
Máximo detalle
```

### Pantalla 13.3" (1920x1080px)
```
[Igual a 7.3" pero con fuentes más grandes]
```

## 🎨 Paleta de Colores

| Uso | Color | Hex | Nota |
|-----|-------|-----|------|
| Fondo | Blanco | #FFFFFF | Base |
| Texto | Negro | #000000 | Principal |
| Bordes | Negro | #000000 | Definición |
| Temperatura Max | Rojo | #d32f2f | Cálido |
| Temperatura Min | Azul | #1976d2 | Frío |
| Fondo tarjeta | Gris claro | #f5f5f5 | Contrast |
| Evento border | Azul | #1976d2 | Acento |
| Evento fondo | Gris suave | #f9f9f9 | Subtle |
| Texto secundario | Gris | #555555 | Subtítulo |

## 🖥️ En E-Ink Real

**Nota importante**: En una pantalla e-ink realmente, los colores se convierten a escala de grises:

```
E-Ink Monocromo:
┌──────────────────────────────────────┐
│      MI CLIMA & AGENDA               │
├─────────────────────────────────────┤
│                                      │
│  6 FEB (Hoy)                         │
│  Parcialmente Nublado                │
│  22°C / 15°C                         │
│                                      │
│  7 FEB (Mañana)                      │
│  Lluvia Ligera                       │
│  18°C / 10°C                         │
│                                      │
│  8 FEB (Viernes)                     │
│  Nublado                             │
│  20°C / 12°C                         │
├─────────────────────────────────────┤
│                                      │
│  • 09:00  Standup del Equipo         │
│  • 10:30  Revisión de Proyecto       │
│  • 14:00  Reunión General Empresa    │
│  • All day Cumpleaños de María       │
│                                      │
└──────────────────────────────────────┘
```

## ✨ Puntos Fuertes del Diseño

✅ **Legibilidad**: Alto contraste, texto grande  
✅ **Minimalismo**: Sin elementos innecesarios  
✅ **Claridad**: Secciones bien separadas  
✅ **Responsive**: Se adapta a cualquier tamaño  
✅ **E-Ink friendly**: Sin gradientes ni complejos  
✅ **Rápido**: Renderiza en < 3 segundos  

## 🔧 Personalización Posible

El usuario puede cambiar:
- ✏️ Título ("Mi Clima & Agenda" → cualquier otro)
- 📍 Ubicación (Lat/Lon)
- 🌡️ Unidades de temperatura
- 📅 Calendarios (agregar/quitar)
- 🎨 Estilos CSS (si quiere customizar)

---

**¿Deseas cambios en el diseño?** Podemos ajustar:
- Tamaño de fuentes
- Proporciones de secciones
- Layout (ej: eventos arriba, clima abajo)
- Número de días mostrados
- Número máximo de eventos
