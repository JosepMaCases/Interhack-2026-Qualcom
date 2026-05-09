<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import maplibregl from 'maplibre-gl';
    
    let {mainMap: maplibregl.Map } = $props(); 
    
    let miniContainer: HTMLDivElement;
    let miniMap: maplibregl.Map;

    function updateViewRect() {
        if (!mainMap || !miniMap || !miniMap.getStyle()) return;

        const source = miniMap.getSource('view-rect') as maplibregl.GeoJSONSource;
        if (!source) return;

        const bounds = mainMap.getBounds();
        const sw = bounds.getSouthWest();
        const ne = bounds.getNorthEast();
        const nw = bounds.getNorthWest();
        const se = bounds.getSouthEast();

        const polygon = {
            type: 'Feature',
            geometry: {
                type: 'Polygon',
                coordinates: [[
                    [sw.lng, sw.lat],
                    [se.lng, se.lat],
                    [ne.lng, ne.lat],
                    [nw.lng, nw.lat],
                    [sw.lng, sw.lat]
                ]]
            }
        };

        source.setData(polygon as any);
        
        miniMap.jumpTo({ 
            center: mainMap.getCenter()
        }); 
    }

    onMount(() => {
        const miniStyle = {
            version: 8,
            sources: {
                'osm-mini': {
                    type: 'vector',
                    url: 'pmtiles://https://www.365-charts.com/protomaps-basemap-opensource-20230408.pmtiles',
                },
                'view-rect': {
                    type: 'geojson',
                    data: { type: 'FeatureCollection', features: [] }
                }
            },
            layers: [
                { 
                    id: 'bg', 
                    type: 'background', 
                    paint: { 'background-color': '#ffffff' } 
                },
                { 
                    id: 'land', 
                    type: 'fill', 
                    source: 'osm-mini', 
                    'source-layer': 'earth', 
                    paint: { 'fill-color': '#d1d5db' }
                },
                {
                    id: 'view-rect-fill',
                    type: 'fill',
                    source: 'view-rect',
                    paint: { 
                        'fill-color': '#ef4444', 
                        'fill-opacity': 0.2 
                    }
                },
                {
                    id: 'view-rect-line',
                    type: 'line',
                    source: 'view-rect',
                    paint: { 
                        'line-color': '#ef4444', 
                        'line-width': 2 
                    }
                }
            ]
        };

        const isMobile = window.innerWidth < 768;
        const initialZoom = isMobile ? -1 : 0;

        miniMap = new maplibregl.Map({
            container: miniContainer,
            style: miniStyle as any,
            center: [0, 0],
            zoom: initialZoom,     
            minZoom: -1,
            interactive: false,
            attributionControl: false
        });

        miniMap.on('style.load', () => {
            miniMap.setProjection({
                type: 'globe'
            });
        });

        miniMap.on('load', () => {
            updateViewRect();
        });

        if (mainMap) {
            mainMap.on('move', updateViewRect);
            mainMap.on('zoom', updateViewRect);
        }
    });

    onDestroy(() => {
        if (miniMap) miniMap.remove();
        if (mainMap) {
            mainMap.off('move', updateViewRect);
            mainMap.off('zoom', updateViewRect);
        }
    });
</script>

<div 
    bind:this={miniContainer} 
    class="mini-map-container"
>
</div>

<style>
    .mini-map-container {
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 60px;
        height: 60px;
        z-index: 50;
        border-radius: 50%; 
        overflow: hidden;
        border: 0.5px solid white;
        box-shadow: 0 1px 2px rgba(0,0,0,0.3); 
    }

    @media (min-width: 768px) {
        .mini-map-container {
            width: 130px;
            height: 130px;
            top: 80px;
            right: 20px;
            border-radius: none;
            border: none !important;
            box-shadow: none; 
        }
    }
</style>