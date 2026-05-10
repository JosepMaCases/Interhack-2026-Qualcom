<script lang="ts">
  import { onMount, onDestroy, createEventDispatcher } from 'svelte';
  import maplibregl from 'maplibre-gl';
  import 'maplibre-gl/dist/maplibre-gl.css';
  import { Protocol } from 'pmtiles';
  import { THEMES } from '$lib/components/molecules/maps/themes';
  import { generateStyleFromTheme } from '$lib/styles/maps/styleFactory';

  let { 
    themeName = 'GLOBE_3D_GREEN', 
    mapInstance = $bindable(),
    children
  } = $props();

  let mapContainer: HTMLDivElement;
  const dispatch = createEventDispatcher();

  onMount(() => {
    if (!maplibregl.config.REGISTERED_PROTOCOLS['pmtiles']) {
        let protocol = new Protocol();
        maplibregl.addProtocol('pmtiles', protocol.tile);
    }

    const theme = THEMES[themeName];
    const style = generateStyleFromTheme(theme);

    const isMobile = window.innerWidth < 768;
    const attribution = isMobile ? false : true;

    mapInstance = new maplibregl.Map({
      container: mapContainer,
      style: style,
      center: theme.center,
      zoom: theme.zoom,
      minZoom: theme.minZoom || 0,
      maxZoom: theme.maxZoom || 20,
      pitch: theme.features.showTerrain ? 60 : 0,
      maxPitch: theme.maxPitch,
      attributionControl: attribution as any,
    });

    mapInstance.addControl( new maplibregl.ScaleControl(),
        'bottom-left'
    );

    mapInstance.on('load', () => {
        if (theme.projection === 'globe') {
            mapInstance?.setProjection({ type: 'globe' });
        }
        dispatch('load', { map: mapInstance });
    });
    
    mapInstance.on('move', () => dispatch('move'));
  });

  onDestroy(() => {
    mapInstance?.remove();
  });
</script>

<div bind:this={mapContainer}>
    {@render children()}
</div>

<style>
    div {
        width: 100%;
        height: 100%;
        background-color: var(--bg-color);
        margin: 0;
    }
    :global(.maplibregl-ctrl-scale) {
      background-color: transparent !important;
      border: none !important;
      border-bottom: 2px solid #444 !important;

      color: #444 !important;
      font-family: 'IBM Plex Sans', sans-serif !important;
    }
</style>

