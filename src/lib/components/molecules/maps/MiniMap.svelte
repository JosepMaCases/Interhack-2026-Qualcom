<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import maplibregl from 'maplibre-gl';
  import 'maplibre-gl/dist/maplibre-gl.css';
  import { Protocol } from 'pmtiles';
  import { generateStyleMini } from '$lib/styles/maps/mapMin'; 

  // --- PROPS PÚBLIQUES ---
  export let boundaryName: string = 'Spain';
  export let center: [number, number] = [-3.7, 40.4];
  export let zoom: number = 4;
  
  let miniMapContainer: HTMLDivElement;
  let miniMap: maplibregl.Map;

  $: if (miniMap && center) {
      miniMap.flyTo({ center: center, zoom: zoom, duration: 1000 });
  }

  $: if (miniMap && miniMap.isStyleLoaded() && boundaryName) {
      if (miniMap.getLayer('boundaries-highlight')) {
          miniMap.setFilter('boundaries-highlight', ['==', 'shapeName', boundaryName]);
      }
  }

  onMount(() => {
    if (!maplibregl.config.REGISTERED_PROTOCOLS || !maplibregl.config.REGISTERED_PROTOCOLS['pmtiles']) {
        let protocol = new Protocol();
        maplibregl.addProtocol('pmtiles', protocol.tile);
    }

    const dynamicStyle = generateStyleMini({
        showBoundaries: true,
        boundarieName: boundaryName,
        backgroundColorMap: '#515050ba',
        showRoads: false,
    });

    miniMap = new maplibregl.Map({
        container: miniMapContainer,
        style: dynamicStyle, 
        center: center, 
        zoom: zoom,    
        interactive: false,
        attributionControl: false
    });
    
    miniMap.on('load', () => {
         if (boundaryName) {
             miniMap.setFilter('boundaries-highlight', ['==', 'shapeName', boundaryName]);
         }
    });
  });

  onDestroy(() => {
    miniMap?.remove();
  });
</script>

<div bind:this={miniMapContainer} class="mini-map-container">
</div>

<style>
  .mini-map-container {
      width: 200px; 
      height: 150px;
      position: absolute;
      top: 20px; 
      right: 20px;
      z-index: 10;
  }
</style>