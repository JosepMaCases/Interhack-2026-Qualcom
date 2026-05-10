<script lang="ts">
  import MapBase from "$lib/components/molecules/maps/MapBase.svelte";
  import MapLayer from "$lib/components/molecules/maps/MapLayer.svelte";

  let mapInstance: any = $state(); 
</script>

<svelte:head>
  <title>Mapa - SafeHelmet</title>
  <meta name="description" content="Visualiza ubicaciones de incidentes y monitoreo en tiempo real." />
</svelte:head>

<div class="map-wrapper">
    <MapBase themeName="CATALONIA_HILLSHADE_BRW_AND_GREEN" bind:mapInstance>
        {#if mapInstance}
            <MapLayer 
                map={mapInstance}
                id="mapa-densitat"
                sourceType="vector"
                type="fill-extrusion"
                url="pmtiles://https://www.365-charts.com/vector_tiles_ghs_pop_2025.pmtiles"
                sourceLayer="mapa_densitat"
                minzoom={8}
                maxzoom={16}
                paint={{
                    'fill-extrusion-color': [
                        'interpolate',
                        ['linear'],
                        ['to-number', ['get', 'DN']],
                        0, '#f3f2e0',  
                        10, '#eccd97', 
                        50, '#8bb19c',  
                        100, '#3c4159',  
                        500, '#d27f65',  
                        1000, '#d27f65' 
                    ],
                    'fill-extrusion-base': 0,
                    'fill-extrusion-height': ['*', ['to-number', ['get', 'DN']], 50], 
                    'fill-extrusion-opacity': .8
                }}
            />
        {/if}
    </MapBase>
</div>

<!-- 
Soroll
Contaminació de l'aire
Accidents de Trànsit
Obres públiques
Congestió de trànsit


-->

<style>
  .map-wrapper {
    width: 100%;
    height: 100vh;
    position: relative;
  }
</style>