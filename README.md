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


**SOFTWARE**

**Entrenament de la IA**

Per a la detecció de col·lisions en temps real amb baixa latència, hem implementat un model de TinyML utilitzant la plataforma Edge Impulse. Això ens permet realitzar l'Edge Computing: el processament de la imatge es fa localment en el dispositiu sense necessitat de dependre del núvol.

Procés d'Entrenament:
- Adquisició de Dades: Creació d'un dataset propi amb més de 100 de captures d'ànecs, realitzades amb la webcam *logi105* de goma en diferents angles, distàncies i condicions de llum per simular obstacles viaris.
- Disseny de l'Impulse: Pre-processat d'imatges per optimitzar el consum de memòria.
- Extracció de característiques mitjançant blocs de processament d'imatge.
- Model de Detecció: Entrenament d'una xarxa neuronal optimitzada per a dispositius mòbils (Object Detection).
- Optimització: Conversió del model a un format lleuger (com TensorFlow Lite) per ser executat en un xip d'alt rendiment i baix consum.
- Implementació Local (On-Device AI): A diferència d'altres sistemes que envien el vídeo a un servidor, la nostra IA corre directament en un microxip dedicat integrat al casc. Això garanteix:

<img width="512" height="512" alt="unknown 6o3ec6b0 ingestion-774b75fcb-lgb7p" src="https://github.com/user-attachments/assets/01041111-9895-4563-ac2f-ebe2a6e025d6" /><img width="512" height="512" alt="unknown 6o3ed6v2 ingestion-774b75fcb-jwg66" src="https://github.com/user-attachments/assets/4cc178a2-95cd-4027-badc-b36ab2577336" />
<img width="512" height="512" alt="unknown 6o3egrjb" src="https://github.com/user-attachments/assets/f84c1097-1ae6-47f5-82ed-4c7452dd2631" />

Característiques del model
- Latència mínima: L'alerta és instantània (crític per evitar col·lisions).
- Privadesa: No s'emmagatzemen ni s'envien imatges de la via pública; el sistema només genera alertes i dades numèriques anònimes.

**PERSPECTIVA DE FUTUR**

Per transformar aquest prototip en un producte de mercat, el nostre full de ruta inclou:
1. IA d'Alt Rendiment i Visió 360°:
- Reconeixement Multiobjecte: Entrenament del model per identificar vehicles, vianants, senyals de trànsit i animals amb un percentatge d'error proper al zero.ç
- Visió Nocturna: Implementació de sensors infrarojos per mantenir la seguretat durant la conducció nocturna o en túnels.

2. Monitorització Ambiental Avançada
- Sensors de Qualitat de l'Aire (NOx, PM2.5): Integració de sensors específics per mesurar partícules en suspensió i diòxid de nitrogen. Això permetria a l'Ajuntament tenir un mapa de contaminació carrer a carrer en temps real.
- Anàlisi de l'Asfalt: Utilitzar l'acceleròmetre per detectar automàticament forats o irregularitats a la calçada i reportar-ho directament als serveis de manteniment urbà.

3. Connectivitat i Ecosistema
- V2X (Vehicle-to-Everything): Connexió directa amb els semàfors i altres vehicles per preveure col·lisions abans que l'objecte sigui visible per la càmera.
- App per a l'Usuari: Una interfície compatible amb dispositius mòbils on el ciclista pugui consultar les seves estadístiques de seguretat i rebre recompenses per les dades ambientals aportades.
