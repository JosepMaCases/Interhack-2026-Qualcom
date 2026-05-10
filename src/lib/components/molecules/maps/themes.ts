export interface MapTheme {
    id: string;
    bounds?: [[number, number], [number, number]];
    center: [number, number];
    zoom: number;
    mobileZoom: number;
    minZoom ?: number;
    maxZoom ?: number;
    maxPitch?: number;
    pitch?: number,
    projection: 'globe' | 'mercator';
    colors: {
        background: string;
        water: string;
        land ?: string,
        boundariesADM0 ?: string,
        boundariesWidthLine ?: number,
        boundariesADM1 ?: string,
        boundariesWidthLine1 ?: number,
        textureOpacity ?: number;
        roads: string;
        roadsLineWidth ?: number;
        roadsOpacity ?: number;
        buildings: string;
        text: string;
    };
    text: {
        textField: string;
        textFont: string;
        textSize: number;
        textAnchor: string;
    }
    features: {
        showTerrain: boolean;
        showRoads: boolean;
        showStreetNames:boolean;
        showBuildings: boolean; 
        showBuildings3D: boolean;
        showCountriesNames: boolean;
        showBoundariesADM0 ?: boolean;
        showBoundariesADM1 ?: boolean;
        showBoundariesADM2 ?: boolean;
        showBoundariesADM3 ?: boolean;
        filterCountry?: string;
        filterIso?: string;
        texture ?: string; // nom del fitxer pmtiles
    };
}

export const THEMES: Record<string, MapTheme> = {
    'CATALONIA_3D_WHITE': {
        id: 'globe-3d-white',
        center: [2.185, 41.403],
        zoom:13.5,
        mobileZoom: 1,
        minZoom: 0,
        maxPitch: 80,
        projection: 'globe',
        colors: {
            background: '#ffffffff',
            water: '#ffffffff',
            boundariesADM0: '#a46347',
            boundariesWidthLine: .6, 
            textureOpacity: 0.6,
            roads: 'rgb(216, 216, 216)',
            roadsLineWidth: 2,
            roadsOpacity: 1,
            buildings: 'rgb(206, 206, 206)',
            text: '#000000ff'
        },
            text: {
            textField: 'name:es',
            textFont: 'IBM-Plex-Sans',
            textSize: 12,
            textAnchor: 'center'
        },
        features: {
            showTerrain: true,
            showRoads: true,
            showStreetNames:true,
            showBuildings: false,
            showBuildings3D: false,
            showCountriesNames: true,
            showBoundariesADM0: true,
            texture:'world_dem_clipped.pmtiles', // nom del fitxer pmtiles
        }
    },
    'CATALONIA_HILLSHADE_BRW_AND_GREEN': {
        id: 'cat-detail',
        bounds: [[0.15, 40.5], [3.35, 42.95]],
        center: [2.185, 41.403],
        zoom: 11.5,
        mobileZoom: 6.5,
        minZoom: 6.5,
        maxPitch: 80,
        projection: 'mercator',
        pitch:60,
        colors: {
            background: '#d7d7d7ff',
            water: '#aaabacff',
            boundariesADM1: '#947454ff',
            boundariesWidthLine1: 0.3,
            textureOpacity: 0.8,
            roads: '#7c7b7bff',
            roadsLineWidth: 1,
            roadsOpacity: 0.7,
            buildings: '#696969ff',
            text: '#000000ff'
        },
            text: {
            textField: 'name:ca',
            textFont: 'IBM-Plex-Sans',
            textSize: 12,
            textAnchor: 'center'
        },
        features: {
            showTerrain: true,
            showRoads: true,
            showStreetNames:true,
            showBuildings: true,
            showBuildings3D: true,
            showCountriesNames: false,
            texture:'cat_arid.pmtiles', // 'texture_grey_min_cat.pmtiles',// nom del fitxer pmtiles
        }
    },

}