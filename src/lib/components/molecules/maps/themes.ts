export interface MapTheme {
    id: string;
    bounds?: [[number, number], [number, number]];
    center: [number, number];
    zoom: number;
    mobileZoom: number;
    minZoom ?: number;
    maxZoom ?: number;
    maxPitch?: number;
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
    'GLOBE_3D_GREEN': {
        id: 'globe-3d-green',
        center: [0, 20],
        zoom:3,
        mobileZoom: 1,
        minZoom: 0,
        maxPitch: 80,
        projection: 'globe',
        colors: {
            background: '#f4f4f4',
            water: '#f4f4f4',
            land: '#f4f4f4',
            boundariesADM0: '#6c7c77', //'#a46347',
            boundariesWidthLine: 1, 
            textureOpacity: 1,
            roads: '#a09f9fff',
            roadsLineWidth: 2,
            roadsOpacity: 1,
            buildings: '#b4b2b2ff',
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
            showRoads: false,
            showStreetNames:false,
            showBuildings:false,
            showBuildings3D: false,
            showCountriesNames: false,
            showBoundariesADM0: true,
            texture:'world_orography.pmtiles', // nom del fitxer pmtiles
        }
    },
    'GLOBE_3D_WHITE': {
        id: 'globe-3d-white',
        center: [0, 20],
        zoom:1,
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
            roads: '#a09f9fff',
            roadsLineWidth: 2,
            roadsOpacity: 1,
            buildings: '#9b9b9bff',
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
            showRoads: false,
            showStreetNames:false,
            showBuildings: true,
            showBuildings3D: false,
            showCountriesNames: true,
            showBoundariesADM0: true,
            texture:'world_dem_clipped.pmtiles', // nom del fitxer pmtiles
        }
    },
    'GLOBE_3D_DARK': {
        id: 'globe-3d-dark',
        center: [0, 20],
        zoom: 1.5,
        mobileZoom: 0,
        minZoom: 0,
        maxPitch: 80,
        projection: 'globe',
        colors: {
            background: '#191919ff',
            water: '#181818ff',
            boundariesADM0: '#e2e2e2ff',
            boundariesWidthLine: 1,
            roads: '#c8c8c8ff',
            roadsLineWidth: 2,
            roadsOpacity: 1,
            buildings: '#b0b0b0ff',
            text: '#bab8b898'
        },
            text: {
            textField: 'name:es',
            textFont: 'IBM-Plex-Sans',
            textSize: 10,
            textAnchor: 'center'
        },
        features: {
            showTerrain: false,
            showRoads: true,
            showStreetNames:true,
            showBuildings: true,
            showBuildings3D: false,
            showCountriesNames: true,
            showBoundariesADM0: true,
        }
    },
    'GLOBE_3D_ADM0': {
        id: 'globe-3d-adm0',
        center: [0, 20],
        zoom: 3,
        mobileZoom: 0,
        minZoom: 3,
        maxPitch: 0,
        projection: 'globe',
        colors: {
            background: '#eaeaeaff',
            water: '#cacacaff',
            boundariesADM0: '#a46347',
            boundariesWidthLine: 0.55, 
            roads: '#727272ff',
            roadsLineWidth: 2,
            roadsOpacity: 1,
            buildings: '#9b9b9bff',
            text: '#000000ff'
        },
            text: {
            textField: 'name:es',
            textFont: 'IBM-Plex-Sans',
            textSize: 12,
            textAnchor: 'center'
        },
        features: {
            showTerrain: false,
            showRoads: false,
            showStreetNames:false,
            showBuildings: false,
            showBuildings3D: false,
            showCountriesNames: true,
            showBoundariesADM0: true,
        }
    },
    'SPAIN_CLEAN': {
        id: 'spain-clean',
        center: [-3, 40],
        zoom: 6,
        mobileZoom: 3,
        minZoom: 6,
        maxPitch: 0,
        projection: 'mercator',
        colors: {
            background: '#c5c4c4ff',
            water: '#c5c4c4ff',
            land: '#ddddddff',
            boundariesADM0: '#a4634709',
            boundariesWidthLine: 1, 
            roads: '#f2f2f3',
            roadsLineWidth: 1,
            roadsOpacity: 1,
            buildings: '#9b9b9bc5',
            text: '#000000ff'
        },
            text: {
            textField: 'name:es',
            textFont: 'IBM-Plex-Sans',
            textSize: 12,
            textAnchor: 'center'
        },
        features: {
            showTerrain: false,
            showRoads: true,
            showStreetNames:true,
            showBuildings: true,
            showBuildings3D: false,
            showCountriesNames: false,
            showBoundariesADM0: true,
            filterCountry: 'Spain',
            filterIso: 'es',
        }
    },
    'SPAIN_CLEAN_MUNICIPALITIES': {
        id: 'spain-clean',
        center: [-3, 40],
        zoom: 6,
        mobileZoom: 3,
        minZoom: 6,
        maxPitch: 0,
        projection: 'mercator',
        colors: {
            background: '#c5c4c4ff',
            water: '#c5c4c4ff',
            land: '#ddddddff',
            boundariesADM0: '#a4634709',
            boundariesWidthLine: 1, 
            roads: '#f2f2f3',
            roadsLineWidth: 1,
            roadsOpacity: 1,
            buildings: '#9b9b9bc5',
            text: '#000000ff'
        },
        text: {
            textField: 'name:es',
            textFont: 'IBM-Plex-Sans',
            textSize: 12,
            textAnchor: 'center'
        },
        features: {
            showTerrain: false,
            showRoads: true,
            showStreetNames:true,
            showBuildings: true,
            showBuildings3D: false,
            showCountriesNames: false,
            showBoundariesADM0: true,
            showBoundariesADM3: false,
            filterCountry: 'Spain',
            filterIso: 'es',
        }
    },
    'CATALONIA_HILLSHADE_BRW_AND_GREEN': {
        id: 'cat-detail',
        bounds: [[0.15, 40.5], [3.35, 42.95]],
        center: [1.735, 41.6975],
        zoom: 8,
        mobileZoom: 6.5,
        minZoom: 6.5,
        maxPitch: 80,
        projection: 'mercator',
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
            showBuildings3D: false,
            showCountriesNames: false,
            texture:'cat_arid.pmtiles', // 'texture_grey_min_cat.pmtiles',// nom del fitxer pmtiles
        }
    },

}