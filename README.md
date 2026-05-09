**POSAR UN NOM DE PROJECTE**

Els usuaris de micro-mobilitat (bicis, patinets) són invisibles a la xarxa viària. La velocitat i la proximitat d'objectes imprevistos causen milers d'accidents anuals per falta de temps de reacció. A més, són un col·lectiu amb més exposició de contaminació de l'aire, cosa que a llarg termini pot provocar problemes greus de salut. 


**QUÈ ÉS ...?**

... és un sistema d'assistència activa i monitorització urbana integrat en cascs de protecció. El projecte neix per resoldre la vulnerabilitat dels ciclistes i usuaris de patinets davant d'objectes estàtics o en moviment en la xarxa viària.
Mitjançant una càmera amb intel·ligència artificial, el casc actua com un "copilot" que vigila l'entorn on la vista de l'usuari no arriba. A més, el dispositiu funciona com una estació mòbil de recollida de dades ambientals, permetent generar un mapa hiper-local de la qualitat de l'aire i de la seguretat viària a Barcelona.

OBJECTIUS DEL PROJECTE: 
- Reduir la sinistralitat: Alertar proactivament sobre possibles col·lisions mitjançant el processament d'imatges en temps real.
- Digitalitzar la seguretat: Identificar punts crítics de la ciutat on es produeixen més frenades brusques o situacions de risc.
- Monitorització Ambiental: Crear un mapa detallat de temperatura i humitat de cada carrer per ajudar als usuaris amb les seves decisionns vials, a més de l'Ajuntament a prendre decisions sobre salut pública.
- Incentivar la mobilitat sostenible: Oferir una eina que aporti prou seguretat perquè més ciutadans s'animin a utilitzar el transport personal no motoritzat.


**COM UTILITZAR-LO?**

L'ecosistema DuckSafe es divideix en tres punts de contacte:
  1. El Casc Intel·ligent: L'usuari només s'ha de posar el casc i iniciar la marxa. El sistema comença a processar el vídeo automàticament.
  2. Sistema d'Alertes (HMI):
     Visual: Un dispositiu instal·lat al manillar emet un parpelleig a una freqüència taronja de 2Hz *epilepsy friendly* quan detecta un perill imminent.
     Sensorial: El casc emet un senyal acústic i una vibració física per assegurar que l'usuari reaccioni en el menor temps possible, fins i tot en entorns amb molt de soroll.
  3. Plataforma Web (Mapa de dades): L'usuari (i l'ajuntament) pot accedir a una aplicació web on es visualitza un mapa interactiu de Barcelona. En aquest mapa es reflecteixen les rutes segures i les dades recollides pels sensors de temperatura i humitat.


**HARDWARE**


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
