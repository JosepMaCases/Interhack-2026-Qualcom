import type { StyleSpecification, LayerSpecification, SourceSpecification, FilterSpecification } from 'maplibre-gl';
import type { MapTheme } from '$lib/components/molecules/maps/themes'; // Assegura't que la ruta és correcta

// URL base del teu bucket R2
const BASE_URL = 'https://www.365-charts.com';

export function generateStyleFromTheme(theme: MapTheme): StyleSpecification {
    const { colors, features, text } = theme;

    const sources: Record<string, SourceSpecification> = {
        'osm-source': {
            type: 'vector',
            url: `pmtiles://${BASE_URL}/protomaps-basemap-opensource-20230408.pmtiles`,
            attribution: '© OpenStreetMap',
            minzoom:2
        }
    };

    if (features.showTerrain) {
        sources['terrain-dem'] = {
            type: 'raster-dem',
            url: 'https://api.maptiler.com/tiles/terrain-rgb/tiles.json?key=Ke2wz8QuYHOCKp3pU3IG',
            tileSize: 512
        };
    }

    if (features.texture) {
        if (theme.id === 'cat-detail') {
            sources['texture'] = {
                type: 'raster',
                url: `pmtiles://${BASE_URL}/${features.texture}`,
                tileSize: 512,
                attribution: 'IGCC'
            };
        } else {
            sources['texture'] = {
                type: 'raster',
                url: `pmtiles://${BASE_URL}/${features.texture}`,
                tileSize: 512,
                attribution: 'GEBECO'
            };
        }
    }

    if (features.showBoundariesADM0) {
        sources['boundaries-ADM0'] = {
            type: 'vector',
            url: `pmtiles://${BASE_URL}/geoBoundariesCGAZ_ADM0.pmtiles`
        };
    }
    if (features.showBoundariesADM1) {
        sources['boundaries-ADM1'] = {
            type: 'vector',
            url: `pmtiles://${BASE_URL}/geoBoundariesCGAZ_ADM1.pmtiles` 
        };
    }
    if (features.showBoundariesADM3) { // Municipis
        sources['boundaries-ADM3'] = {
            type: 'vector',
            url: `pmtiles://${BASE_URL}/municipalities_spain.pmtiles` 
        };
    }

    const layers: LayerSpecification[] = [];
    layers.push({
        id: 'background',
        type: 'background',
        paint: { 'background-color': colors.background }
    });


    if (colors.land && colors.land !== 'transparent') {
         layers.push({
            id: 'land-base',
            type: 'fill',
            source: 'osm-source',
            'source-layer': 'earth',
            paint: { 'fill-color': colors.land }
        });
    }

    layers.push({
        id: 'water',
        type: 'fill',
        source: 'osm-source',
        'source-layer': 'water',
        paint: { 'fill-color': colors.water }
    });

    if (features.texture) {
        layers.push({
            id: 'texture-layer',
            type: 'raster',
            source: 'texture',
            paint: { 
                'raster-opacity': colors.textureOpacity ?? 0.6,
            }
        });
    }

    if (features.showBoundariesADM3) {
        layers.push({
            id: 'boundaries-adm3',
            type: 'line',
            source: 'boundaries-ADM3',
            'source-layer': 'ADM3',
            paint: {
                'line-color': colors.boundariesADM0 || '#ccc', 
                'line-width': 0.5,
                'line-opacity': 0.5
            }
        });
    }

    if (features.showBoundariesADM1) {
        layers.push({
            id: 'boundaries-adm1',
            type: 'line',
            source: 'boundaries-ADM1',
            'source-layer': 'ADM1',
            paint: {
                'line-color': colors.boundariesADM1 || colors.boundariesADM0 || '#888',
                'line-width': colors.boundariesWidthLine1 || 0.5,
                'line-opacity': 1
            }
        });
    }

    if (features.showBoundariesADM0) {
        layers.push({
            id: 'boundaries-adm0',
            type: 'line',
            source: 'boundaries-ADM0',
            'source-layer': 'ADM0',
            ...(features.filterCountry && { 
                filter: ['==', 'shapeName', features.filterCountry] 
            }), 
            paint: {
                'line-color': colors.boundariesADM0 || '#444',
                'line-width': colors.boundariesWidthLine || 1,
                'line-opacity': 1
            }
        });
    }

    if (features.showRoads) {
        layers.push({
            id: 'roads',
            type: 'line',
            source: 'osm-source',
            'source-layer': 'roads',
            paint: {
                'line-color': colors.roads,
                'line-width': colors.roadsLineWidth || 1,
                'line-opacity': colors.roadsOpacity || 1
            }
        });
    }

    if (features.showBuildings) {
        if (features.showBuildings3D) {
            layers.push({
                id: 'buildings-3d',
                type: 'fill-extrusion',
                source: 'osm-source',
                'source-layer': 'buildings',
                paint: {
                    'fill-extrusion-color': colors.buildings,
                    'fill-extrusion-height': ['get', 'height'], 
                    'fill-extrusion-base': 0,
                    'fill-extrusion-opacity': 0.9
                }
            });
        } else {
            layers.push({
                id: 'buildings-2d',
                type: 'fill',
                source: 'osm-source',
                'source-layer': 'buildings',
                paint: {
                    'fill-color': colors.buildings,
                    'fill-opacity': 1
                }
            });
        }
    }

    if (features.showCountriesNames) {
         layers.push({
            id: 'country-labels',
            type: 'symbol',
            source: 'osm-source',
            'source-layer': 'places',
            filter: ['==', 'place', 'country'],
            layout: {
                'text-field': ['coalesce', ['get', text.textField]],
                'text-font': [text.textFont],
                'text-size': text.textSize, 
                'text-transform': 'uppercase',
                'text-letter-spacing': 0.1,
                'text-anchor': 'center'
            },
            paint: {
                'text-color': colors.text,
                'text-halo-color': 'white',
                'text-halo-width': 1
            }
        });
    }

    layers.push({
        id: 'place-labels',
        type: 'symbol',
        source: 'osm-source',
        'source-layer': 'places',
        filter: [
            'all',
            ['>', 'pmap:rank', 0],
            ['!=', 'place', 'country']
        ],
        layout: {
            'text-field': ['coalesce', ['get', text.textField], ['get', 'name:en'], ['get', 'name']],
            'text-font': [text.textFont],
            'text-size': text.textSize,
            'text-anchor': text.textAnchor as any
        },
        paint: {
            'text-color': colors.text,
            'text-halo-color': 'white',
            'text-halo-width': 1
        }
    });

    if (features.showStreetNames) {
        layers.push({
            id:'roads-labels',
            type: 'symbol',
            source:'osm-source',
            'source-layer':'roads',
            minzoom:12,
            filter: [
                'all',
                ['has', 'name']
            ],
            layout: {
                'symbol-placement':'line',
                'text-field': ['coalesce', ['get', text.textField], ['get', 'name']],
                'text-font':[text.textFont],
                'text-size':12,
                'text-letter-spacing':0.1,
                'text-max-angle': 30
            },
            paint: {
                'text-color':colors.text,
                'text-halo-color':'white',
                'text-halo-width': 2
            }
        });
    }

    return {
        version: 8,
        glyphs: `${BASE_URL}/fonts/{fontstack}/{range}.pbf`,
        sources: sources,
        layers: layers,
        terrain: features.showTerrain 
            ? { source: 'terrain-dem', exaggeration: 2.5 } 
            : undefined
    };
}