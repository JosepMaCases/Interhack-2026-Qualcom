<script lang="ts">
  import MapBase from "$lib/components/molecules/maps/MapBase.svelte";
  import MapLayer from "$lib/components/molecules/maps/MapLayer.svelte";

  let mapInstance: any = $state(); 

  // 1. Definimos el estado de los toggles para cada capa
  let activeLayers = $state({
    densitat: true,   // La que ya tenías
    soroll: false,    // Tipo Raster
    aire: false,      // Tipo Polígono (fill)
    accidents: false, // Tipo Círculo (circle)
    obres: true,     // Tipo Polígono (fill)
    congestio: false  // Tipo Línea (line)
  });
</script>

<svelte:head>
  <title>Mapa - SafeHelmet</title>
  <meta name="description" content="Visualiza ubicaciones de incidentes y monitoreo en tiempo real." />
</svelte:head>

<div class="map-wrapper">
    
    <div class="layer-controls">
        <label>
            <input type="checkbox" bind:checked={activeLayers.soroll} /> 
            Contaminación acústica
        </label>
        <label>
            <input type="checkbox" bind:checked={activeLayers.aire} /> 
            Contaminació de l'aire
        </label>
        <label>
            <input type="checkbox" bind:checked={activeLayers.accidents} /> 
            Accidents de trànsit
        </label>
        <label>
            <input type="checkbox" bind:checked={activeLayers.obres} /> 
            Obres públiques
        </label>
    </div>

    <MapBase themeName="CATALONIA_3D_WHITE" bind:mapInstance>
        {#if mapInstance}
            {#if activeLayers.soroll}
                <MapLayer 
                    map={mapInstance}
                    id="mapa-soroll"
                    sourceType="raster"
                    type="raster"
                    url="URL_DE_TU_FUENTE_RASTER_SOROLL"
                    paint={{
                        'raster-opacity': 0.6,
                        'raster-contrast': 0.2
                    }}
                />
            {/if}

            {#if activeLayers.aire}
                <MapLayer 
                    map={mapInstance}
                    id="mapa-aire"
                    sourceType="vector"
                    type="fill"
                    url="URL_DE_TU_FUENTE_AIRE"
                    sourceLayer="aire_layer"
                    paint={{
                        'fill-color': [
                            'interpolate', ['linear'], ['get', 'aqi_value'],
                            0, '#00e400',  // Bueno
                            50, '#ffff00', // Moderado
                            100, '#ff7e00', // Dañino para grupos sensibles
                            150, '#ff0000'  // Dañino
                        ],
                        'fill-opacity': 0.4
                    }}
                />
            {/if}

            {#if activeLayers.accidents}
                <MapLayer 
                    map={mapInstance}
                    id="mapa-accidents"
                    sourceType="vector"
                    type="circle"
                    url="URL_DE_TU_FUENTE_ACCIDENTES"
                    sourceLayer="accidents_layer"
                    paint={{
                        'circle-radius': ['interpolate', ['linear'], ['zoom'], 10, 3, 15, 8],
                        'circle-color': '#e74c3c',
                        'circle-stroke-width': 2,
                        'circle-stroke-color': '#ffffff'
                    }}
                />
            {/if}

            {#if activeLayers.obres}
                <MapLayer 
                    map={mapInstance}
                    id="mapa-obres"
                    sourceType="vector"
                    type="fill"
                    url="pmtiles://https://www.365-charts.com/obres_bcn_2026.pmtiles"
                    sourceLayer="mapa_obres_corregido"
                    paint={{
                        'fill-color': '#f39c12',
                        'fill-outline-color': '#d35400',
                        'fill-opacity': 0.5
                    }}
                />
            {/if}
        {/if}
    </MapBase>
</div>

<style>
  .map-wrapper {
    width: 100%;
    height: 100vh;
    position: relative;
  }
  .layer-controls {
    position: absolute;
    top: 6rem;
    left: 20px;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 10;
    display: flex;
    flex-direction: column;
    gap: 10px;
    backdrop-filter: blur(4px);
  }

  .layer-controls label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.95rem;
    color: var(--second-color);
    cursor: pointer;
    font-family: sans-serif;
    user-select: none;
  }

  .layer-controls input[type="checkbox"] {
    cursor: pointer;
    width: 16px;
    height: 16px;
  }
</style>