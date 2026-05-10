# SafeHelmet - Sistema de Detecció de Col·lisions

**Nom del Projecte**: SafeHelmet

## 🎯 Objectius del Projecte

- Elaborar un sistema de detecció de col·lisió i alerta d'objectes estàtics i dinàmics, integrat en cascos de protecció homologats com a eina accessòria en la circulació
- Detectar objectes en moviment simulant la realitat de la xarxa viària
- Resoldre el risc que implica l'exces de velocitat i proximitat d'objectes

## 🏗️ Arquitectura Web

La interfície web ha estat principalment estructurada amb:

### Pàgines i Rutes (SEO Optimitzat)
- **`/`** - Pàgina d'inici amb una introducció del producte
- **`/map`** - Visualització d'ubicacions, incidents i altres dades
- **`/camera`** - Monitoratge en viu amb detecció activa
- **`/about`** - Informació sobre el projecte i l'equip

### Components Principals

#### Capçalera Millorada
- 3 columnes: Botó Mapa | Logo  | About Us + Menú
- Navegació intuïtiva
- Capçalera sticky en desplaçament

#### Barra Lateral
- Menú contextual (~25% d'amplada)
- Només visible a `/map` i `/camera`
- Transicions suaus
- Overlay per tancar

#### Disseny Modern
- Gradients de color (Taronja #ff3e00 → Groc #ffaa00)
- Transicions i efectes hover
- Disseny responsiu (Escriptori, Tauleta, Mòbil)

## 💻 Tecnologies Utilitzades

### Frontend
- **Svelte 5.55.2** - Framework reactiu
- **SvelteKit 2.57.0** - Framework full-stack amb enrutament
- **TypeScript 6.0.2** - Tipatge estàtic
- **Vite 8.0.7** - Eina de build ràpida

### Backend (Arduino)
- **Python** - Script principal
- **Arduino IDE** - Sketch de hardware
- Detecció de col·lisions mitjançant sensors

## 🚨 Sistemes d'Alerta

### Alerta Lluminosa
- Parpelleig de dos hertzos
- LED no saturat en vermell
- Ubicat al manillar

### Alerta Sonora i Vibració
- Sistema integrat al casc
- Notificació immediata de proximitat

### Detecció Intel·ligent
- Identificació de distàncies amb OpenCV (implementable)
- Anàlisi de velocitat d'objectes
- Sistema en temps real

## 📁 Estructura del Projecte

```
Interhack-2026-Qualcom/
├── src/
│   ├── routes/                    # Rutes SvelteKit
│   │   ├── +layout.svelte        # Layout principal
│   │   ├── +page.svelte          # Landing
│   │   ├── map/+page.svelte      # Mapa
│   │   ├── about/+page.svelte    # Informació
│   │   └── camera/+page.svelte   # Monitoratge en viu
│   ├── lib/
│   │   ├── components/
│   │   │   └── molecules/templates/
│   │   │       ├── Header.svelte       # Capçalera millorada
│   │   │       ├── Sidebar.svelte      # Menú lateral
│   │   │       ├── About.svelte        # Pàgina about
│   │   │       └── MapLayout.svelte    # Layout del mapa
│   │   └── styles/
│   │       └── global.css              # Estils globals
│   └── static/icons/             # Icones SVG
├── Arduino code/
│   ├── sketch/
│   │   └── sketch.ino            # Codi Arduino
│   └── python/
│       └── main.py               # Script Python
├── package.json
└── svelte.config.js

```

## 🚀 Com Executar

### Desenvolupament
```bash
npm install      # Instal·lar dependències
npm run dev      # Iniciar servidor (http://localhost:5173)
```

### Build per a Producció
```bash
npm run build    # Crear build optimitzat
npm run preview  # Veure la previsualització del build
```

### Validació
```bash
npm run check          # Svelte check
npm run check:watch    # Check en mode watch
```

## 🎨 Paleta de Colors

| Color | Ús | Valor |
|-------|-----|-------|
| Taronja | Principal (Botons, Enllaços) | #ff3e00 |
| Groc | Secundari (Gradients) | #ffaa00 |
| Gris Clar | Fons | #f4f4f4 |
| Gris Fosc | Text | #272727 |

## 🔄 Flux de Navegació

```
Inici (/)
    ↓
[Explorar Mapa] [Saber Més]
    ↓                ↓
  /map            /about
  ├─ Header       ├─ Header
  ├─ Menú ✓       ├─ Menú ✗
  └─ MapLayout    └─ Informació

Des de /map:
  ↓ (Botó Menú)
[Barra Lateral] - 25% d'amplada
  - Settings
  - Documentation
  - Support
  - Contact
```

## ✨ Característiques Destacades

✅ **SEO Optimitzat** - Meta tags i títols a cada pàgina
✅ **Responsiu** - Funciona en tots els dispositius
✅ **Transicions Suaus** - Animacions fade entre pàgines
✅ **Menú Condicional** - Només visible on correspon
✅ **Capçalera Sticky** - S'adapta al desplaçament
✅ **Interactivitat** - Efectes hover i animacions

## 📝 Properes Millores

- [ ] Integrar mapa real (Leaflet/Mapbox)
- [ ] Websocket per a dades en viu
- [ ] Dashboard d'estadístiques
- [ ] Sistema d'autenticació
- [ ] Galeria de productes
- [ ] Animació 3D del casc

## 🤝 Col·laboradors

- Equip d'Interhack 2026
- Qualcomm Innovation Challenge

---

**Última actualització**: 10 de maig de 2026
 

Evolució: 

Les proximes etapes del producte es centraran principalment en l'escalabilitat i la incorporació de sistemas de llum infraroiga per poder millorar la il·luminació o fins i tot permetre la circulació nocturna


**SOFTWARE**

**Entrenament de la IA**

Per a la detecció de col·lisions en temps real amb baixa latència, hem implementat un model de TinyML utilitzant la plataforma Edge Impulse. Això ens permet realitzar Edge Computing. El processament de  imatges es fa localment en el dispositiu sense necessitat de dependre del núvol aprofitant un model local.

Procés d'Entrenament:
- Adquisició de Dades: Creació d'un dataset propi amb més de 100 de captures d'ànecs de goma, realitzades amb la webcam *Logitech Brio 105 Business Webcam* diferents angles. Considerant factor com les distàncies i condicions de llum per simular obstacles variads.
- Disseny de l'Impulse: Pre-processat d'imatges per optimitzar el consum de memòria.
- Extracció de característiques mitjançant blocs de processament d'imatge.
- Model de Detecció: Entrenament d'una xarxa neuronal optimitzada per a dispositius mòbils (Object Detection).
- Optimització: Conversió del model a un format lleuger (equivalent TensorFlow Lite) per ser executat en un xip d'alt rendiment i baix consum.
- Implementació Local (On-Device AI): A diferència d'altres sistemes que envien el vídeo a un servidor, la nostra IA corre directament en un microxip dedicat integrat al casc.

<img width="512" height="512" alt="unknown 6o3ec6b0 ingestion-774b75fcb-lgb7p" src="https://github.com/user-attachments/assets/01041111-9895-4563-ac2f-ebe2a6e025d6" /><img width="512" height="512" alt="unknown 6o3ed6v2 ingestion-774b75fcb-jwg66" src="https://github.com/user-attachments/assets/4cc178a2-95cd-4027-badc-b36ab2577336" />
<img width="512" height="512" alt="unknown 6o3egrjb" src="https://github.com/user-attachments/assets/f84c1097-1ae6-47f5-82ed-4c7452dd2631" />

Característiques del model
- Latència mínima: L'alerta és instantània (crític per evitar col·lisions).
- Privadesa: No s'emmagatzemen ni s'envien imatges de la via pública; el sistema només genera alertes i dades numèriques anònimes.

-Resultat del model. Com que el nostre producte requereix de mesura les distancies amb els objectes, utilitzarem com a refèrencia la ratio de tamany del objecte respecte a la image complerta. Com que aquesta ratio té que variar amb propocio a la distancia, els entrenaments dels que disposabem (Orientats a treballar amb centroides) son ineficients i per tant el model no ens ha donat els resultats desitjats.

Com a consequencia hem utilitzat un model previament entrenat per la compañia Qualcomm Innovation Challenge per a la realització de la nostra demo.

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
