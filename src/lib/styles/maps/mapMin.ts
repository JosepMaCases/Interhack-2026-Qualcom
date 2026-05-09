import type { StyleSpecification, SourceSpecification, LayerSpecification, FilterSpecification } from 'maplibre-gl';

export interface MapConfig {
    showBoundaries: boolean;
    boundarieName: string;
    showRoads?: boolean;
    backgroundColorMap: string
}

export function generateStyleMini(config: MapConfig): StyleSpecification {
    const {
        showBoundaries = true,
        boundarieName = 'Spain', 
        backgroundColorMap = '#515050ba',
        showRoads = false,
    } = config;

    const sources: { [key: string]: SourceSpecification } = {
        'boundaries-ADM0': {
            type: 'vector',
            url: 'pmtiles://https://www.365-charts.com/geoBoundariesCGAZ_ADM0.pmtiles'
        },
        ...(showRoads ? {
            'roads-osm': {
                type: 'vector',
                url: 'pmtiles://...' 
            }
        } : {})
    };

    const layers: LayerSpecification[] = [ 
        {
            id: 'background',
            type: 'background',
            paint: { 
                'background-color': 'rgba(0, 0, 0, 0)' 
            }
        },
        ...(showBoundaries ? [{
            id: 'boundaries-highlight',
            type: 'fill',
            source: 'boundaries-ADM0',
            'source-layer': 'ADM0',
            filter: ['==', 'shapeName', boundarieName], 
            paint: {
                'fill-color': backgroundColorMap,
                'fill-opacity': 1,
                'fill-outline-color': '#ffffff'
            }
        } as LayerSpecification] : []),

        ...(showRoads ? [{
            id: 'roads',
            type: 'line',
            source: 'roads-osm',
            'source-layer': 'roads',
            paint: {
                'line-color': '#ffffffba',
                'line-width': 0.3,
                'line-opacity': 1
            }
        } as LayerSpecification] : [])
    ];

    return {
        version: 8,
        sources: sources,
        layers: layers
    };
}