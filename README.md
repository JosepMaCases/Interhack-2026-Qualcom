# SafeHelmet - Sistema de Detección de Colisiones

**Nombre del Proyecto**: SafeHelmet

## 🎯 Objetivos del Proyecto

- Elaborar un sistema de detección de colisión e alerta de objetos estáticos y en movimiento integrado en cascos de protección homologados como herramienta accesoria en la circulación
- Detectar objetos en movimiento simulando una realidad de la red viaria
- Resolver el problema de velocidad y proximidad de objetos

## 🏗️ Arquitectura Web

La interfaz web ha sido completamente reestructurada con:

### Páginas y Rutas (SEO Optimizado)
- **`/`** - Landing page con introducción
- **`/map`** - Visualización de ubicaciones e incidentes
- **`/camera`** - Monitoreo en vivo con detección activa
- **`/about`** - Información del proyecto y equipo

### Componentes Principales

#### Header Mejorado
- 3 columnas: Botón Mapa | Logo Centrado | About Us + Menú
- Navegación intuitiva
- Header sticky en scroll

#### Sidebar Lateral
- Menú contextual (~25% ancho)
- Solo visible en `/map` y `/camera`
- Transiciones suaves
- Overlay para cerrar

#### Diseño Moderno
- Gradientes de color (Naranja #ff3e00 → Amarillo #ffaa00)
- Transiciones y hover effects
- Responsive design (Desktop, Tablet, Mobile)

## 💻 Tecnologías Utilizadas

### Frontend
- **Svelte 5.55.2** - Framework reactivo
- **SvelteKit 2.57.0** - Full-stack framework con routing
- **TypeScript 6.0.2** - Tipado estático
- **Vite 8.0.7** - Build tool rápido

### Backend (Arduino)
- **Python** - Script principal
- **Arduino IDE** - Sketch de hardware
- Detección de colisiones mediante sensores

## 🚨 Sistemas de Alerta

### Alerta Lumínica
- Parpadeo de dos herzios
- LED no saturado en rojo
- Ubicado en el manillar

### Alerta Sonora y Vibración
- Sistema integrado en el casco
- Notificación inmediata de proximidad

### Detección Inteligente
- Identificación de distancias con OpenCV (implementable)
- Análisis de velocidad de objetos
- Sistema en tiempo real

## 📁 Estructura del Proyecto

```
Interhack-2026-Qualcom/
├── src/
│   ├── routes/                    # Rutas SvelteKit
│   │   ├── +layout.svelte        # Layout principal
│   │   ├── +page.svelte          # Landing
│   │   ├── map/+page.svelte      # Mapa
│   │   ├── about/+page.svelte    # Información
│   │   └── camera/+page.svelte   # Monitoreo en vivo
│   ├── lib/
│   │   ├── components/
│   │   │   └── molecules/templates/
│   │   │       ├── Header.svelte       # Header mejorado
│   │   │       ├── Sidebar.svelte      # Menú lateral
│   │   │       ├── About.svelte        # Página about
│   │   │       └── MapLayout.svelte    # Layout del mapa
│   │   └── styles/
│   │       └── global.css              # Estilos globales
│   └── static/icons/             # Iconos SVG
├── Arduino code/
│   ├── sketch/
│   │   └── sketch.ino            # Código Arduino
│   └── python/
│       └── main.py               # Script Python
├── package.json
└── svelte.config.js

```

## 🚀 Cómo Ejecutar

### Desarrollo
```bash
npm install      # Instalar dependencias
npm run dev      # Iniciar servidor (http://localhost:5173)
```

### Build para Producción
```bash
npm run build    # Crear build optimizado
npm run preview  # Ver preview del build
```

### Validación
```bash
npm run check          # Svelte check
npm run check:watch    # Check en modo watch
```

## 🎨 Paleta de Colores

| Color | Uso | Valor |
|-------|-----|-------|
| Naranja | Principal (Botones, Links) | #ff3e00 |
| Amarillo | Secundario (Gradientes) | #ffaa00 |
| Gris Claro | Fondo | #f4f4f4 |
| Gris Oscuro | Texto | #272727 |

## 🔄 Flujo de Navegación

```
Inicio (/)
    ↓
[Explorar Mapa] [Saber Más]
    ↓                ↓
  /map            /about
  ├─ Header       ├─ Header
  ├─ Menú ✓       ├─ Menú ✗
  └─ MapLayout    └─ Información

Desde /map:
  ↓ (Botón Menú)
[Sidebar Lateral] - 25% ancho
  - Settings
  - Documentation
  - Support
  - Contact
```

## ✨ Características Destacadas

✅ **SEO Optimizado** - Meta tags y titles en cada página
✅ **Responsive** - Funciona en todos los dispositivos
✅ **Transiciones Suaves** - Fade animations entre páginas
✅ **Menú Condicional** - Solo visible donde corresponde
✅ **Header Sticky** - Se adapta al scroll
✅ **Interactividad** - Hover effects y animaciones

## 📝 Próximas Mejoras

- [ ] Integrar mapa real (Leaflet/Mapbox)
- [ ] Websocket para datos en vivo
- [ ] Dashboard de estadísticas
- [ ] Sistema de autenticación
- [ ] Galería de productos
- [ ] Animación 3D del casco

## 🤝 Contribuidores

- Equipo de Interhack 2026
- Qualcomm Innovation Challenge

---

**Última actualización**: 9 de Mayo de 2026
 

Evolution: 

Escalable, posar la llum infraroja per lloc pocs il·luminats. 


Logo: pato de goma con gorra

