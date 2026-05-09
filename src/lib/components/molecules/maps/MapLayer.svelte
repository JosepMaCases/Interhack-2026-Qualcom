<script lang="ts">
    import type { Map, AddLayerObject } from 'maplibre-gl';
    let {
        map, 
        id: layerId,
        sourceType,
        type, 
        
        data = undefined,
        url = undefined,
        tiles = undefined,
        videoUrls = undefined,
        coordinates = undefined,

        minzoom = undefined,
        maxzoom = undefined,
        tileSize = 512,
        bounds = undefined, // [num, num, num, num]

        paint = {},
        layout = {},
        filter = undefined,
        sourceLayer = undefined,
        beforeId = undefined,
        opacity = 1
    } = $props<{
        map: Map | any; 
        id: string;
        sourceType: 'vector' | 'raster' | 'geojson' | 'video' | 'image';
        type: 'fill' | 'line' | 'symbol' | 'circle' | 'heatmap' | 'fill-extrusion' | 'raster' | 'hillshade' | 'background';
        
        data?: any | string;
        url?: string;
        tiles?: string[];
        videoUrls?: string[];
        coordinates?: number[][]; // [[lng,lat], [lng,lat]...]
        
        minzoom?: number;
        maxzoom?: number;
        tileSize?: number;
        bounds?: [number, number, number, number];

        paint?: any;
        layout?: any;
        filter?: any[];
        sourceLayer?: string;
        beforeId?: string;
        opacity?: number;
    }>();

    $effect(() => {
        if (!map || !map.getStyle()) return;
        const sourceId = layerId;

        if (!map.getSource(sourceId)) {
            const sourceConfig: any = { type: sourceType };
            if (sourceType === 'geojson') {
                sourceConfig.data = data;
            } 
            else if (sourceType === 'vector' || sourceType === 'raster') {
                if (url) sourceConfig.url = url; 
                if (tiles) sourceConfig.tiles = tiles; 
                if (tileSize) sourceConfig.tileSize = tileSize;
                if (bounds) sourceConfig.bounds = bounds;
            } 
            else if (sourceType === 'image') {
                sourceConfig.url = url;
                sourceConfig.coordinates = coordinates;
            }
            else if (sourceType === 'video') {
                sourceConfig.urls = videoUrls || (url ? [url] : []);
                sourceConfig.coordinates = coordinates;
            }
            if (minzoom !== undefined) sourceConfig.minzoom = minzoom;
            if (maxzoom !== undefined) sourceConfig.maxzoom = maxzoom;

            map.addSource(sourceId, sourceConfig);
        }

        if (!map.getLayer(layerId)) {
            const layerConfig: AddLayerObject = {
                id: layerId,
                type: type,
                source: sourceId,
                paint: paint,
                layout: layout
            };

            if (sourceLayer) layerConfig['source-layer'] = sourceLayer;
            if (minzoom !== undefined) layerConfig.minzoom = minzoom;
            if (maxzoom !== undefined) layerConfig.maxzoom = maxzoom;

            map.addLayer(layerConfig, beforeId);
            
            if (opacity !== 1 && map.setPaintProperty) {
                const opacityProp = `${type}-opacity`;
                try {
                    map.setPaintProperty(layerId, opacityProp, opacity);
                } catch (e) {

                }
            }
        }

        return () => {
            if (map.getLayer(layerId)) map.removeLayer(layerId);
            if (map.getSource(sourceId)) map.removeSource(sourceId);
        };
    });
</script>